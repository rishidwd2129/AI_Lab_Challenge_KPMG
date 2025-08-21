import json
from Call_llm import LLM_Pipeline

try:
    llm_handler = LLM_Pipeline(model_id = "Qwen/Qwen2-1.5B-Instruct")
except Exception as e:
    print(f"Error initializing LLM Pipeline: {e}")
    llm_handler = None

def llm_extract_graph(text_chunk: str) -> list[dict]:
    """
    Extracts graph triples from a text chunk using an LLM.
    
    Args:
        text_chunk (str): The text from which to extract triples.
    
    Returns:
        list[dict]: A list of extracted triples in the format {'subject': str, 'predicate': str, 'object': str}.
    """
    if not llm_handler:
        print("LLM handler is not initialized. Cannot extract graph.")
        return []

    prompt = f"""From the following text,extract up to 5 key entities and their relationships.
    Respond ONLY with a valid JSON object containing a single key "triples". The value should be a list of lists,
    where each inner list is a triple: [head_entity, relationship, tail_entity].
    Do not add any explanation, preamble, or summary.

    Text: "{text_chunk}"
    """
    
    try:
        # prompt = f"Extract triples from the following text:\n{text_chunk}\nFormat: {{'subject': '...', 'predicate': '...', 'object': '...'}}"
        response = llm_handler.call_llm(prompt)
        triples = json.loads(response[0]['generated_text'][0]['content'])
        return triples
    except Exception as e:
        print(f"Error extracting graph: {e}")
        return []
    

# --- Main Execution Block for Testing ---
if __name__ == "__main__":
    print("\n--- Running standalone test for llm_extract_graph ---")
    
    # 1. Define a sample text chunk for extraction
    sample_text = """
    Apple Inc., headquartered in Cupertino, announced that Tim Cook, its CEO, 
    would be presenting at the annual Worldwide Developers Conference (WWDC). 
    The conference highlights new software, including updates to iOS, which runs on the iPhone.
    """
    
    # 2. Call the function to extract the graph data
    print(f"\nInput Text:\n{sample_text}")
    extracted_triples = llm_extract_graph(sample_text)
    
    # 3. Print the results in a readable format
    print("\n--- Extraction Results ---")
    if extracted_triples:
        print("Successfully extracted the following triples:")
        for i, triple in enumerate(extracted_triples, 1):
            print(f"  {i}. {triple}")
    else:
        print("No triples were extracted from the text.")
    
    print("\n--- Test Complete ---")
