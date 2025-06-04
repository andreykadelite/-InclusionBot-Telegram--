import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'inclusion.db'

conn = sqlite3.connect(DB_PATH)

# Ensure tables exist
with conn:
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        contact TEXT,
        needs TEXT,
        role TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        status TEXT DEFAULT 'open'
    )
    ''')

def add_user(user_id: int, name: str, department: str, contact: str, needs: str, role: str='employee'):
    with conn:
        conn.execute(
            'REPLACE INTO users(user_id, name, department, contact, needs, role) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, name, department, contact, needs, role)
        )

def get_user(user_id: int):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    return cur.fetchone()

def add_request(user_id: int, text: str):
    with conn:
        cur = conn.execute('INSERT INTO requests(user_id, text) VALUES(?, ?)', (user_id, text))
        return cur.lastrowid

def list_user_requests(user_id: int):
    cur = conn.cursor()
    cur.execute('SELECT id, text, status FROM requests WHERE user_id=?', (user_id,))
    return cur.fetchall()

