def py():
    return None
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "certs.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                course TEXT NOT NULL,
                date_text TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
        """)
        conn.commit()

def insert_certificate(full_name: str, course: str, date_text: str, email: str, file_path: str) -> int:
    created_at = datetime.now().isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO certificates (full_name, course, date_text, email, created_at, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (full_name, course, date_text, email, created_at, file_path))
        conn.commit()
        return cur.lastrowid