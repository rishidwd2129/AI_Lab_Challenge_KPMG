import re
import json
from Action.Tool import read_google_sheet, get_highest_sale_record, search_recent_company_news, create_google_doc, tools
from Call_llm import LLM_Pipeline
from SystemPrompt import DocTemplate

class AgentExecutor:
    def __init__(self, tools: list, pipe):
        """Initializes the executor with a tool registry."""
        self.tools = {tool.name: tool for tool in tools}
        self.pipe = pipe
        print("Executor initialized with the following tools:", list(self.tools.keys()))

    # THIS IS THE UPGRADED METHOD THAT FIXES THE BUG
    def _resolve_params(self, params: dict, step_outputs: dict) -> dict:
        resolved_params = {}
        for key, value in params.items():
            if isinstance(value, str):
                # This is the pattern for a standalone reference
                standalone_pattern = r"^\$ref\.step_(\d+)\.output(?:\.([\w_]+))?$"
                match = re.match(standalone_pattern, value)

                if match:
                    # CASE 1: The entire value is a reference. Return the raw object.
                    step_num = int(match.group(1))
                    key_path = match.group(2)
                    
                    referenced_output = step_outputs.get(step_num)
                    if key_path:
                        resolved_params[key] = referenced_output.get(key_path)
                    else:
                        resolved_params[key] = referenced_output
                else:
                    # CASE 2: The value contains one or more embedded references.
                    # Use re.sub to find and replace them with string versions.
                    embedded_pattern = r"\$ref\.step_(\d+)\.output(?:\.([\w_]+))?"
                    
                    def repl_func(m):
                        step_num = int(m.group(1))
                        key_path = m.group(2)
                        
                        ref_output = step_outputs.get(step_num)
                        if key_path:
                            return str(ref_output.get(key_path, ''))
                        else:
                            if isinstance(ref_output, list):
                                return "\n- ".join(map(str, ref_output))
                            return str(ref_output)
                    
                    resolved_params[key] = re.sub(embedded_pattern, repl_func, value)
            else:
                # If the value is not a string, keep it as is.
                resolved_params[key] = value
                
        return resolved_params

    # The rest of your execute_plan method is correct and does not need to be changed.
    def execute_plan(self, plan: dict) -> any:
        # ... (your existing execute_plan code) ...
        # ... (it will now work correctly with the fix above) ...
        if "plan" not in plan:
            raise ValueError("Invalid plan format. Missing 'plan' key.")

        step_outputs = {}
        sorted_plan = sorted(plan["plan"], key=lambda x: x["step"])
        TOP_RESULT:dict
        for step in sorted_plan:
            step_num = step["step"]
            tool_name = step["tool"]
            params = step["params"]
            summary = step["summary"]
            
            print(f"\n--- Executing Step {step_num}: {summary} ---")
            
            if tool_name not in self.tools:
                raise ValueError(f"Tool '{tool_name}' not found in the registry.")

            resolved_params = self._resolve_params(params, step_outputs)
            
            if step["tool"] == "create_google_doc":
                print("------------Generating LLM Summary------------")
                # Assuming DocTemplate and self.pipe.call_llm are correctly defined elsewhere
                llm_input = DocTemplate(title=resolved_params['title'], content=resolved_params['content'], Sheet_Data= TOP_RESULT)
                llm_response = self.pipe.call_llm(messages=[{"role": "user", "content": llm_input}], max_output=1000)
                llm_response = llm_response[0]['generated_text'][1]['content']
                resolved_params['content'] = llm_response
                print(f"LLM Generated Content: {llm_response}")

            print(f"  Calling tool '{tool_name}' with params: {resolved_params}")

            tool_to_call = self.tools[tool_name]
            result = tool_to_call.invoke(resolved_params)
            
            if step["tool"] == "get_highest_sale_record":
                TOP_RESULT = result
            
            step_outputs[step_num] = result
            print(f"  Step {step_num} Output: {result}")
        
        final_result = step_outputs.get(len(plan["plan"]))
        return final_result

# --- Main Orchestration Logic ---
if __name__ == "__main__":
    # 1. The JSON plan you received from the Planner
    generated_plan = {
      "plan": [
        {
          "step": 1,
          "tool": "read_google_sheet",
          "params": { "file_name": "Q3 Sales" },
          "summary": "Read the sales data from the 'Q3 Sales' Google Sheet."
        },
        {
          "step": 2,
          "tool": "get_highest_sale_record",
          "params": { "data": "$ref.step_1.output" },
          "summary": "Identify the company with the highest sales from the sheet data."
        },
        {
          "step": 3,
          "tool": "search_recent_company_news",
          "params": { "company_name": "$ref.step_2.output.company" },
          "summary": "Search for recent news about the top-performing company."
        },
        {
          "step": 4,
          "tool": "create_google_doc",
          "params": {
            "title": "Q3 Sales Summary for $ref.step_2.output.company",
            "content": "Combine the sales data from step 2 and the news from step 3 into a summary document."
          },
          "summary": "Create a Google Doc summarizing the top company's performance and news."
        }
      ]
    }

    # 2. Define the list of all available tools
    all_tools = [
        read_google_sheet,
        get_highest_sale_record,
        search_recent_company_news,
        create_google_doc
    ]
    
    # 3. Instantiate and run the Executor
    executor = AgentExecutor(tools=tools)
    final_result = executor.execute_plan(generated_plan)
    
    print("\n" + "="*50)
    print("       Agent Execution Finished ")
    print("="*50)
    print("Final Result:")
    print(final_result)
    print("="*50)
