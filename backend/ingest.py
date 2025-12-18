import os
import uuid
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

COLLECTION = "rag_prod"

# Create collection if not exists
if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

def ingest_folder(folder_path, role):
    for file in os.listdir(folder_path):
        if not file.endswith(".pdf"):
            continue

        reader = PdfReader(os.path.join(folder_path, file))
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue

            vector = model.encode(text).tolist()

            client.upsert(
                collection_name=COLLECTION,
                points=[
                    {
                        "id": str(uuid.uuid4()),  # ✅ SAFE ID
                        "vector": vector,
                        "payload": {
                            "text": text,
                            "allowed_role": role,
                            "source": file
                        }
                    }
                ]
            )

# Ingest documents by role
ingest_folder("data/docs/hr", "HR")
ingest_folder("data/docs/finance", "FINANCE")
ingest_folder("data/docs/ops", "OPS")

print("Documents ingested successfully")
