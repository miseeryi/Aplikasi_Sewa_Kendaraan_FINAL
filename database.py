import sqlite3
import hashlib

DB_NAME = "rental.db"

def connect():
    return sqlite3.connect(DB_NAME)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def ensure_admin():
    conn = connect()
    cur = conn.cursor()

    username = "admin"
    pwd_hash = hash_password("admin123")

    cur.execute("SELECT id FROM admin WHERE username=?", (username,))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO admin(username, password_hash) VALUES (?,?)",
            (username, pwd_hash)
        )

    conn.commit()
    conn.close()