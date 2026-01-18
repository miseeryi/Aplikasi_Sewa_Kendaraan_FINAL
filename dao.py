# from database import connect

# # ---- Kendaraan ----
# def kendaraan_all():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("SELECT id, tipe, plat, merk, tarif FROM kendaraan ORDER BY id DESC")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def kendaraan_insert(tipe, plat, merk, tarif):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO kendaraan(tipe, plat, merk, tarif) VALUES(?,?,?,?)",
#                 (tipe, plat, merk, tarif))
#     conn.commit()
#     conn.close()

# def kendaraan_update(id_, tipe, plat, merk, tarif):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("UPDATE kendaraan SET tipe=?, plat=?, merk=?, tarif=? WHERE id=?",
#                 (tipe, plat, merk, tarif, id_))
#     conn.commit()
#     conn.close()

# def kendaraan_delete(id_):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM kendaraan WHERE id=?", (id_,))
#     conn.commit()
#     conn.close()


# # ---- Pelanggan ----
# def pelanggan_all():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("SELECT id, nama, telp FROM pelanggan ORDER BY id DESC")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def pelanggan_insert(nama, telp):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO pelanggan(nama, telp) VALUES(?,?)", (nama, telp))
#     conn.commit()
#     conn.close()

# def pelanggan_update(id_, nama, telp):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("UPDATE pelanggan SET nama=?, telp=? WHERE id=?", (nama, telp, id_))
#     conn.commit()
#     conn.close()

# def pelanggan_delete(id_):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM pelanggan WHERE id=?", (id_,))
#     conn.commit()
#     conn.close()


# # ---- Sewa ----
# def sewa_all_join():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("""
#     SELECT s.id, s.tanggal, s.durasi, s.total,
#            k.tipe, k.plat, k.merk, k.tarif,
#            p.id, p.nama, p.telp
#     FROM sewa s
#     JOIN kendaraan k ON k.id = s.kendaraan_id
#     JOIN pelanggan p ON p.id = s.pelanggan_id
#     ORDER BY s.id DESC
#     """)
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def sewa_insert(kendaraan_id, pelanggan_id, tanggal, durasi, total):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO sewa(kendaraan_id, pelanggan_id, tanggal, durasi, total) VALUES(?,?,?,?,?)",
#         (kendaraan_id, pelanggan_id, tanggal, durasi, total)
#     )
#     conn.commit()
#     conn.close()

from database import connect, hash_password


def admin_login(username, password):
    conn = connect()
    cur = conn.cursor()


    pwd_hash = hash_password(password)


    cur.execute(
        "SELECT id FROM admin WHERE username=? AND password_hash=?",
        (username, pwd_hash)
    )
    row = cur.fetchone()
    conn.close()


    return row is not None

# ========== KENDARAAN ==========
# def kendaraan_all():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("SELECT id, tipe, plat, merk, tarif FROM kendaraan ORDER BY id DESC")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def kendaraan_insert(tipe, plat, merk, tarif):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO kendaraan(tipe, plat, merk, tarif) VALUES(?,?,?,?)",
#         (tipe, plat, merk, tarif)
#     )
#     conn.commit()
#     conn.close()

# def kendaraan_update(id_, tipe, plat, merk, tarif):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute(
#         "UPDATE kendaraan SET tipe=?, plat=?, merk=?, tarif=? WHERE id=?",
#         (tipe, plat, merk, tarif, id_)
#     )
#     conn.commit()
#     conn.close()

# def kendaraan_delete(id_):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM kendaraan WHERE id=?", (id_,))
#     conn.commit()
#     conn.close()


# ========== PELANGGAN ==========
# def pelanggan_all():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("SELECT id, nama, telp FROM pelanggan ORDER BY id DESC")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def pelanggan_insert(nama, telp):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO pelanggan(nama, telp) VALUES(?,?)", (nama, telp))
#     conn.commit()
#     conn.close()

# def pelanggan_update(id_, nama, telp):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("UPDATE pelanggan SET nama=?, telp=? WHERE id=?", (nama, telp, id_))
#     conn.commit()
#     conn.close()

# def pelanggan_delete(id_):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM pelanggan WHERE id=?", (id_,))
#     conn.commit()
#     conn.close()


# # ========== SEWA ==========
# def sewa_all_join():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT s.id, s.tanggal, s.durasi, s.total,
#                k.tipe, k.plat, k.merk,
#                p.nama, p.telp
#         FROM sewa s
#         JOIN kendaraan k ON k.id = s.kendaraan_id
#         JOIN pelanggan p ON p.id = s.pelanggan_id
#         ORDER BY s.id DESC
#     """)
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def sewa_insert(kendaraan_id, pelanggan_id, tanggal, durasi, total):
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO sewa(kendaraan_id, pelanggan_id, tanggal, durasi, total) VALUES(?,?,?,?,?)",
#         (kendaraan_id, pelanggan_id, tanggal, durasi, total)
#     )
#     conn.commit()
#     conn.close()

   
