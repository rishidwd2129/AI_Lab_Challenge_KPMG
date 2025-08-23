from Call_llm import LLM_Pipeline
from SystemPrompt import PlannerTemplate


pipe = LLM_Pipeline()

def call_planner(user_query: str) -> str:
    Input = PlannerTemplate(user_query)
    response = pipe.Gemini_API(Input)
    return response


if __name__ == "__main__":
    prompt = "Analyze the Q3 Sales sheet, find the top company, search for news, and create a summary doc."
    response = call_planner(prompt)
    print(type(response))  # This will print the type of the response
    print(f"response for the Planner is : --------------------\n{response}")  # This will print the response from the LLM
    