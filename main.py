from Call_llm import LLM_Pipeline
from Executor import AgentExecutor
from Planner import call_planner
from Action.Tool import tools
from TextProcessor.String2Json import to_Json
from SystemPrompt import RouterTemplate


def main():
    pipe = LLM_Pipeline(model_id="Qwen/Qwen2-1.5B-Instruct")
    executor = AgentExecutor(tools=tools, pipe=pipe)
    # Chat Loop
    while True:
        Query = input("Enter your query (or 'q' to quit): ") 
        if Query.lower() == 'q':
            # Exit chat 
            break
        # print(f"User Query: {Query}")
        # Call Router to get the plan or to directly generate answers
        routerInput = RouterTemplate(Query)
        routerResponse = pipe.Gemini_API(routerInput)
        routerResponse = to_Json(routerResponse)
        print(routerResponse.get("route"))
        # 2. Execute the correct path based on the router's decision
        if routerResponse.get("route") == "planner":
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
        else:
            response = pipe.call_llm(Query)
            print(50*"=")
            print("---------------Direct LLM Response---------------")
            print(f"LLM Response:{response}")

if __name__ == "__main__":
    main()
