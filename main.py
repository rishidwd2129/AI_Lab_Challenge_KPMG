from Call_llm import LLM_Pipeline
from Executor import AgentExecutor
from Planner import call_planner
from Action.Tool import tools
from TextProcessor.String2Json import to_Json


def main():
    pipe = LLM_Pipeline(model_id="Qwen/Qwen2-1.5B-Instruct")
    executor = AgentExecutor(tools=tools, pipe=pipe)
    # loop for chat
        # 1. Initialize the LLM pipeline
        #get input, 
        # form input create Prompt
        # use planner promt to input planner to create plan 
        #  use output json to Call tools 
        # consolidate outputs form the tools and create the final prompt and then make the final LLM call
    # Chat Loop started
    while True:
        Query = input("Enter your query (or 'q' to quit): ")  
        if Query.lower() == 'q':
            # Exit chat 
            break
        print(f"User Query: {Query}")
        # 2. Call the planner to get the JSON plan
        plan = call_planner(Query, pipe)
        # string to Json 
        plan = to_Json(plan)
        print(50*"=")
        print(type(plan))
        print(f"Parsed Plan: {plan}")
        print(50*"=")
        # Execute the generated plan
        executor.execute_plan(plan)

if __name__ == "__main__":
    main()
