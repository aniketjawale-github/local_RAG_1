from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.rag import rag_answer
from backend.db import cursor, conn


app = FastAPI(title="Local RAG API")

# ---------- Request schema ----------
class AskRequest(BaseModel):
    email: str
    question: str


# ---------- API endpoint ----------
@app.post("/ask")
def ask_rag(req: AskRequest):
    # 1. Get user role
    cursor.execute(
        "SELECT role FROM users WHERE email = ?",
        (req.email,)
    )
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="User not authorized")

    role = row[0]

    # 2. Get RAG answer
    answer = rag_answer(req.question, role)

    # 3. Log question
    cursor.execute(
        "INSERT INTO logs (user_email, question) VALUES (?, ?)",
        (req.email, req.question)
    )
    conn.commit()

    return {
        "email": req.email,
        "role": role,
        "answer": answer
    }
