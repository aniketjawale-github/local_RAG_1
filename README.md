# 🧠 Fully Local RAG System with Role-Based Access Control

## 📌 Project Overview

This project is a **fully local Retrieval-Augmented Generation (RAG) system** built from scratch using **only free and open-source tools**.

It allows employees to ask natural-language questions from **company documents (PDFs)** and receive **accurate answers strictly from authorized data**, enforced using **role-based access control (FGAC)**.

🚫 No cloud  
🚫 No OpenAI  
🚫 No external APIs  
✅ Everything runs on localhost  

---

## 🎯 Why This Project Exists

In many companies:
- Data exists in PDFs, SOPs, policies, reports
- Employees manually search files
- Answers depend on people, not systems
- Sensitive data must not leak across departments

This system solves that by:
- Turning documents into a searchable knowledge base
- Enforcing department-level access
- Providing instant answers
- Keeping all data inside the organization

---

## ✅ What This System Does

- Reads PDFs from local folders
- Converts documents into semantic vectors
- Stores vectors in a local vector database
- Allows users to ask questions
- Retrieves only relevant document chunks
- Enforces role-based document access
- Generates answers using a **local LLM**
- Provides a simple chat UI

---

## 🏗️ High-Level Architecture

User
↓
Streamlit UI
↓
FastAPI Backend
↓
SQLite (User → Role mapping)
↓
Sentence-Transformers (Text → Vectors)
↓
Qdrant (Vector search + role filtering)
↓
Ollama (Local LLM)
↓
Answer



## 🛠️ Tools Used (What & Why)

| Layer | Tool | Purpose |
|---|---|---|
| UI | Streamlit | Simple chat interface |
| Backend | FastAPI | Central controller |
| User DB | SQLite | Store users, roles, logs |
| PDF Reader | PyPDF | Extract text from PDFs |
| Chunking | Custom Python | Full control |
| Embeddings | Sentence-Transformers | Convert text → vectors |
| Vector DB | Qdrant | Semantic search + FGAC |
| LLM | Ollama (LLaMA) | Local answer generation |
| Container | Docker | Run Qdrant locally |

---

## 📂 Project Structure

local_rag/
├── backend/
│ ├── main.py # FastAPI backend
│ ├── rag.py # RAG logic (retrieve + generate)
│ ├── ingest.py # PDF ingestion pipeline
│ ├── db.py # SQLite DB
│ └── seed_users.py # Sample users
├── ui/
│ └── app.py # Streamlit chat UI
├── data/
│ └── docs/
│ ├── hr/
│ ├── finance/
│ └── ops/
├── requirements.txt
└── README.md

## 🔄 End-to-End Working (Runtime Flow)

### 1️⃣ System Startup
- Ollama runs local LLM (`localhost:11434`)
- Qdrant runs vector DB (`localhost:6333`)
- FastAPI runs backend (`localhost:8000`)
- Streamlit runs UI (`localhost:8501`)

All are **separate processes**.

---

### 2️⃣ Document Ingestion (Before Usage)

1. PDFs are read using PyPDF
2. Each PDF page becomes **one chunk**
3. Each chunk is converted into a vector
4. Vector + metadata (role, source) stored in Qdrant

This builds the **knowledge base**.

---

### 3️⃣ User Asks a Question

Example:
What is the leave policy?

User enters:
- Email
- Question

---

### 4️⃣ Backend Processing

FastAPI:
1. Receives request
2. Looks up user role in SQLite
3. Converts question to vector
4. Queries Qdrant **with role filter**
5. Retrieves top-K relevant chunks

---

### 5️⃣ Vector Search + FGAC (Critical)

Inside Qdrant:
- Only vectors with `allowed_role = user_role` are searched
- Unauthorized documents are never accessed

This is **fine-grained access control at data level**.

---

### 6️⃣ Answer Generation

1. Retrieved chunks are combined as context
2. Context + question sent to Ollama
3. Ollama generates answer **only from context**
4. No hallucination, no external knowledge

---

### 7️⃣ Response & Logging

- Answer returned to Streamlit UI
- Question logged in SQLite
- User sees final answer

---

## 🔐 Role-Based Access Control (FGAC)

- Each document chunk has metadata:
  - `allowed_role`
- Qdrant enforces access **during retrieval**
- UI cannot bypass backend
- Backend cannot bypass Qdrant filters

Example:
- HR user → HR documents only
- Finance user → Finance documents only

---

## 🧪 Sample Users

| Email | Role |
|---|---|
| hr@company.com | HR |
| finance@company.com | FINANCE |
| ops@company.com | OPS |
| manager@company.com | MANAGER |

---

## ▶️ How to Run Locally

### 1️⃣ Start Qdrant
```
docker run -p 6333:6333 qdrant/qdrant
2️⃣ Start Ollama
bash
Copy code
ollama run llama3.1:8b
3️⃣ Ingest Documents
bash
Copy code
python backend/ingest.py
4️⃣ Start Backend
bash
Copy code
uvicorn backend.main:app --reload
5️⃣ Start UI

Copy code
streamlit run ui/app.py
🧠 What You Learn from This Project
How RAG works internally

How embeddings & vectors behave

How vector databases perform search

How FGAC is enforced correctly

How to build secure AI systems

How to run LLMs locally

How real production RAG systems are designed

🧩 Key Takeaway
This project demonstrates a real, production-style RAG architecture built fully locally, showing how documents, vectors, access control, and LLMs work together end-to-end.

🔮 Possible Next Enhancements
JWT authentication

Token-based chunking with overlap

Feedback loop (👍 / 👎)

DEV / PROD separation

Docker-compose (one-command start)

Cloud migration (Azure / AWS)
