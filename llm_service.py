import requests
from config import OLLAMA_BASE_URL, EMBEDDING_MODEL, CHAT_MODEL


def get_embeddings(text: str) -> list:
    # enerate embeddings using nomic-embed-text model
    url = f"{OLLAMA_BASE_URL}/embeddings"
    
    try:
        response = requests.post(
            url,
            json={"model": EMBEDDING_MODEL, "prompt": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("embedding", [])
    except Exception as e:
        print(f"Embedding error: {e}")
        return []


def ask_llm(question: str, context: str) -> str:
    print("Asking LLM with context...",question, context)
    #generate answer using llama model
    url = f"{OLLAMA_BASE_URL}/generate"
    
    prompt = f"""Based on the following data, answer the question concisely and accurately.

Data:
{context}

Question: {question}

Answer:"""
    
    try:
        response = requests.post(
            url,
            json={"model": CHAT_MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "Could not generate answer.")
    except Exception as e:
        return f"LLM Error: {str(e)}"
