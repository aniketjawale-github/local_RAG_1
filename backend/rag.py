
from sentence_transformers import SentenceTransformer
import requests

# Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

QDRANT_URL = "http://localhost:6333"
COLLECTION = "rag_prod"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


def call_llm(context, question):
    prompt = f"""
You are a company assistant.
Answer ONLY using the context below.
If the answer is not present, say:
"Information not available in company documents."

Context:
{context}

Question:
{question}
"""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def search_qdrant(vector, role):
    """Direct REST call to Qdrant search API"""
    response = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
        json={
            "vector": vector,
            "limit": 5,
            "with_payload": True,
            "filter": {
                "must": [
                    {
                        "key": "allowed_role",
                        "match": {
                            "value": role
                        }
                    }
                ]
            }
        }
    )
    response.raise_for_status()
    return response.json()["result"]


def rag_answer(question, role):
    # Convert question to vector
    query_vector = embed_model.encode(question).tolist()

    # Search Qdrant (FGAC enforced)
    results = search_qdrant(query_vector, role)

    if not results:
        return "Information not available in company documents."

    # Build context
    context = " ".join([hit["payload"]["text"] for hit in results])

    # Generate answer from local LLM
    return call_llm(context, question)
