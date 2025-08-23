import json
def to_Json(llm_output: str) -> dict:
    """
    Cleans and parses a string containing a JSON object by finding the first
    opening brace and the last closing brace.
    """
    try:
        # Find the first opening brace
        start_index = llm_output.find('{')
        
        # FIX: Use rfind() to get the LAST closing brace in the string
        end_index = llm_output.rfind('}')
        
        # If either brace isn't found, handle the error
        if start_index == -1 or end_index == -1:
            print("Error: Could not find a valid JSON object in the string.")
            return {}
            
        # Extract the full JSON string and parse it
        cleaned_string = llm_output[start_index : end_index + 1]
        data = json.loads(cleaned_string)
        return data
        
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from the extracted string. Error: {e}")
        return {}

if __name__ == "__main__":


  llm_output = '''json
{
  "plan": [
    {
      "step": 1,
      "tool": "search_recent_company_news",
      "params": {
        "company_name": "KPMG"
      },
      "summary": "Search for the latest financial news about KPMG."
    }
  ]
}Json
'''
  parsed_plan = to_Json(llm_output)
  # Pretty-print the successfully parsed dictionary
  print(type(parsed_plan))
  print(json.dumps(parsed_plan, indent=2))






  #   llm_output = """
#   json
# {
#   "plan": [
#     {
#       "step": 1,
#       "tool": "search_recent_company_news",
#       "params": {
#         "company_name": "KPMG"
#       },
#       "summary": "Search the web for the latest news about KPMG."
#     },
#     {
#       "step": 2,
#       "tool": "create_google_doc",
#       "params": {
#         "title": "Latest Financial News about KPMG",
#         "content": "$ref.step_1.output"
#       },
#       "summary": "Create a Google Doc containing the gathered news about KPMG."
#     }
#   ]
# } Json
# """