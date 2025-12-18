from backend.db import cursor, conn

users = [
    ("hr@company.com", "HR"),
    ("finance@company.com", "FINANCE"),
    ("ops@company.com", "OPS"),
    ("manager@company.com", "MANAGER")
]

for email, role in users:
    try:
        cursor.execute(
            "INSERT INTO users (email, role) VALUES (?, ?)",
            (email, role)
        )
    except:
        pass  # ignore if already exists

conn.commit()
print("Users added")
