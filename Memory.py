from langchain.memory import ConversationBufferMemory
# from Retriver import simple_similarity_search
from SystemPrompt import RagTemplate
from Call_llm import LLM_Pipeline

class MemoryManager:
    def __init__(self, llm_pipeline: LLM_Pipeline ):
        """
        Initializes the MemoryManager with a given LLM pipeline.
        """
        print("Initializing Memory Manager")
        self.llm_pipeline = llm_pipeline
        self.memory = ConversationBufferMemory( return_messages=True)
        print("Memory Manager initialized successfully!")
              
    def _get_formatted_history(self):
        return self.memory.load_memory_variables({})['history']
    
    # def chat(self, user_input: str):
        # Performing similarity search on Database
        Context_Response = simple_similarity_search(user_input)

        context = Context_Response.data[0]['content'] if Context_Response and Context_Response.data else "No relevant context found."

        # Create the final Prompt
        input_prompt = RagTemplate(query=user_input, context=context)
        print("Step 3: Prompt template created.")
        # 1. Load the current chat history
        history_message = self._get_formatted_history()
        # 2. Create teh prompt for the LLM
        # the prompt now includes the history and the new user input
        # your Qwen model expects a list of directories
        messages= [
            #  Convert langchain message objects to dictionaries
            {"role":"system","content":"You are a helpful assistant."},
        ]
        for msg in history_message:
            #  LangChain stores messages as AIMessage or HumanMessage
            role = "user" if "Human" in msg.type else "assistant"
            messages.append({"role": role, "content": msg.content})

        #  Add the new user input
        messages.append({"role": "user", "content": input_prompt})

        # 3 . calls the original .call_llm() method
        response = self.llm_pipeline.call_llm(messages)
        # Extract the actual text content from the model's output
        ai_response = response[0]["generated_text"][-1]["content"]

        self.memory.save_context({"input": user_input}, {"output": ai_response})

        return ai_response
    
if __name__ == "__main__":
    llm_pipe = LLM_Pipeline()
    # 2. Initialize the MemoryManager with the pipeline
    chat_manager = MemoryManager(llm_pipeline=llm_pipe)

    print("\n--- Chatbot is Ready ---")
    print("Type 'quit' or 'exit' to end the conversation.")
    
    # 3. Start an infinite loop for the chat
    while True:
        # 4. Get input from the user
        user_query = input("\nEnter your query : ")

        # 5. Check for exit condition
        if user_query.lower() in ['quit', 'exit']:
            print("AI: Goodbye!")
            break
        
        # 6. Get the chatbot's response and print it
        ai_reply = chat_manager.chat(user_query)
        print(ai_reply)