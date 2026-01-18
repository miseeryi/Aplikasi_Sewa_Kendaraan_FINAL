# import sqlite3
# import hashlib


# DB_NAME = "rental.db"

# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()

# def ensure_admin():

#     conn = connect()
#     cur = conn.cursor()

#     username = "admin"
#     password_hash = hash_password("admin123")

#     cur.execute("SELECT id FROM admin WHERE username=?", (username,))
#     exists = cur.fetchone()

#     if not exists:
#         cur.execute(
#             "INSERT INTO admin(username, password_hash) VALUES (?,?)",
#             (username, password_hash)
#         )

#     conn.commit()
#     conn.close()


# def connect():
#     return sqlite3.connect(DB_NAME)

# def init_db():
#     conn = connect()
#     cur = conn.cursor()
    
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS admin (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password_hash TEXT NOT NULL   
#     );
#     """)

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS kendaraan(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         tipe TEXT NOT NULL,           -- MOBIL / MOTOR
#         plat TEXT NOT NULL UNIQUE,
#         merk TEXT NOT NULL,
#         tarif INTEGER NOT NULL
#     )
#     """)

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS pelanggan(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nama TEXT NOT NULL,
#         telp TEXT NOT NULL
#     )
#     """)

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS sewa(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         kendaraan_id INTEGER NOT NULL,
#         pelanggan_id INTEGER NOT NULL,
#         tanggal TEXT NOT NULL,        -- yyyy-mm-dd
#         durasi INTEGER NOT NULL,
#         total INTEGER NOT NULL,
#         FOREIGN KEY(kendaraan_id) REFERENCES kendaraan(id),
#         FOREIGN KEY(pelanggan_id) REFERENCES pelanggan(id)
#     )
#     """)

#     conn.commit()
#     conn.close()

import sqlite3
import hashlib

DB_NAME = "rental.db"

# def connect():
#     return sqlite3.connect(DB_NAME)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def init_db():
#     conn = connect()
#     cur = conn.cursor()

    # cur.execute("""
    # CREATE TABLE IF NOT EXISTS admin (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     username TEXT UNIQUE NOT NULL,
    #     password_hash TEXT NOT NULL
    # )
    # """)

    # conn.commit()
    # conn.close()

# def ensure_admin():
#     conn = connect()
#     cur = conn.cursor()

#     username = "admin"
#     pwd_hash = hash_password("admin123")

#     cur.execute("SELECT id FROM admin WHERE username=?", (username,))
#     if not cur.fetchone():
#         cur.execute(
#             "INSERT INTO admin(username, password_hash) VALUES (?,?)",
#             (username, pwd_hash)
#         )

#     conn.commit()
#     conn.close()
