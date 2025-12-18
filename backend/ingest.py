import os
import uuid
import pandas as pd
from pypdf import PdfReader
from docx import Document
from PIL import Image
import pytesseract
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from faster_whisper import WhisperModel

# -----------------------------
# OCR CONFIG
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------
# MODELS & CLIENTS
# -----------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

whisper_model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

qdrant = QdrantClient(host="localhost", port=6333)

COLLECTION = "rag_prod"

if not qdrant.collection_exists(COLLECTION):
    qdrant.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

# -----------------------------
# EXTRACTORS
# -----------------------------
def extract_pdf(path):
    reader = PdfReader(path)
    return [p.extract_text() for p in reader.pages if p.extract_text()]

def extract_csv(path):
    df = pd.read_csv(path)
    return [df.to_string(index=False)]

def extract_excel(path):
    df = pd.read_excel(path)
    return [df.to_string(index=False)]

def extract_docx(path):
    doc = Document(path)
    return [p.text for p in doc.paragraphs if p.text.strip()]

def extract_image(path):
    text = pytesseract.image_to_string(Image.open(path))
    return [text] if text.strip() else []

def extract_audio(path):
    segments, _ = whisper_model.transcribe(path, beam_size=5, language="en")

    texts, buffer = [], ""
    for seg in segments:
        buffer += seg.text.strip() + " "
        if len(buffer) > 800:
            texts.append(buffer.strip())
            buffer = ""

    if buffer.strip():
        texts.append(buffer.strip())

    return texts

# -----------------------------
# FILE ROUTER
# -----------------------------
def extract_text(file_path):
    path = file_path.lower()

    if path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif path.endswith(".csv"):
        return extract_csv(file_path)
    elif path.endswith(".xlsx"):
        return extract_excel(file_path)
    elif path.endswith(".docx"):
        return extract_docx(file_path)
    elif path.endswith((".png", ".jpg", ".jpeg")):
        return extract_image(file_path)
    elif path.endswith((".mp3", ".wav")):
        return extract_audio(file_path)
    else:
        return []

# -----------------------------
# INGESTION
# -----------------------------
def ingest_role_folder(base_path, role):
    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            texts = extract_text(file_path)

            for text in texts:
                if not text.strip():
                    continue

                vector = embed_model.encode(text).tolist()

                qdrant.upsert(
                    collection_name=COLLECTION,
                    points=[{
                        "id": str(uuid.uuid4()),
                        "vector": vector,
                        "payload": {
                            "text": text,
                            "allowed_role": role,
                            "source": file_path,
                            "file_type": os.path.splitext(file)[1]
                        }
                    }]
                )

# -----------------------------
# INGEST BY ROLE
# -----------------------------
ingest_role_folder("data/docs/hr", "HR")
ingest_role_folder("data/docs/finance", "FINANCE")
ingest_role_folder("data/docs/ops", "OPS")

print("✅ All documents (including audio) ingested successfully")
