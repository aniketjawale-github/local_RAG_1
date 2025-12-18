# 🔍 Local RAG System with Role-Based Access (Fully Offline)

## 📌 Project Overview

This project is a **fully local Retrieval-Augmented Generation (RAG) system** that allows users to ask questions from company documents (PDFs) and receive accurate answers **only from authorized data**, with **no cloud services involved**.

The system enforces **role-based access control (RBAC / FGAC)**, ensuring that users can only query documents relevant to their department (HR, Finance, Operations, etc.).

All components run **locally on a single machine**, making it suitable for learning, demos, and small internal company deployments.

---

## 🚀 What This System Does

- Reads company PDFs (policies, SOPs, reports)
- Converts documents into semantic embeddings
- Stores embeddings in a vector database
- Allows users to ask natural language questions
- Retrieves only relevant document chunks
- Enforces role-based document access
- Generates answers using a **local LLM**
- Provides a simple chat UI

---

## 🧠 Key Features

- ✅ Fully local (no OpenAI / no cloud)
- ✅ Free & open-source tools only
- ✅ Role-based access control (FGAC)
- ✅ Secure document-level filtering
- ✅ No hallucinations (answers only from docs)
- ✅ Production-style architecture
- ✅ Decoupled UI and backend

---

## 🏗️ Solution Architecture

