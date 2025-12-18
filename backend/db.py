import sqlite3

# Create / connect to local DB file
conn = sqlite3.connect("backend/rag.db", check_same_thread=False)

cursor = conn.cursor()

# Users table (for roles)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    role TEXT
)
""")

# Logs table (for audit)
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    question TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
