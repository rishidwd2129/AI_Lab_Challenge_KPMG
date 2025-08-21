# # 1. The updated mock database
# mock_sheets_db = {
#     "Q3 Sales": [
#         {"company": "Innovate Inc.", "sales": 500000},
#         {"company": "QuantumLeap Co.", "sales": 850000},
#         {"company": "DataWeavers", "sales": 620000},
#         {"company": "AlphaTech", "sales": 780000},
#         {"company": "KPMG", "sales": 950000},
#         {"company": "Solutions Hub", "sales": 450000},
#         {"company": "NextGen Partners", "sales": 890000}
#     ]
# }

# # 2. Access the list of sales data from the database
# sales_data = mock_sheets_db["Q3 Sales"]
# # print(type(mock_sheets_db))

# # 3. Find the record with the highest sales
# # The `max()` function is used with a 'key' to specify that we should
# # compare the dictionaries based on their 'sales' value.
# highest_sales_record = max(sales_data, key=lambda record: record['sales'])
# print(type(highest_sales_record))
# # 4. Print the result
# # print("Record with the highest sales:")
# # print(highest_sales_record)

# from langchain_google_genai import ChatGoogleGenerativeAI

# # This replaces your entire LLM_Pipeline class for the agent
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="get me latest financial news about KPMG"
)
print(response.text)


# print(response)