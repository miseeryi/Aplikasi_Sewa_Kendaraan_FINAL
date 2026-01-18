import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date

from database import init_db, ensure_admin
from database import init_db, connect
from models.mobil import Mobil
from models.motor import Motor
                
init_db()
ensure_admin()

# ---------- Helper DB ----------
# def fetch_all_kendaraan():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("SELECT id, tipe, plat, merk, tarif FROM kendaraan ORDER BY id DESC")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

import dao

# def fetch_all_kendaraan():
#     # ambil data kendaraan via DAO (SRP: query dipisah)
#     return dao.kendaraan_all()

def fetch_all_kendaraan():
    return dao.kendaraan_all()

def fetch_all_pelanggan():
    return dao.pelanggan_all()

def fetch_all_sewa():
    return dao.sewa_all_join()



# def k_refresh():
#     ...
#     for row in dao.kendaraan_all():
#         ...


# def fetch_all_pelanggan():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("SELECT id, nama, telp FROM pelanggan ORDER BY id DESC")
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# def fetch_all_sewa():
#     conn = connect()
#     cur = conn.cursor()
#     cur.execute("""
#     SELECT s.id, s.tanggal, s.durasi, s.total,
#            k.tipe, k.plat, k.merk,
#            p.nama, p.telp
#     FROM sewa s
#     JOIN kendaraan k ON k.id = s.kendaraan_id
#     JOIN pelanggan p ON p.id = s.pelanggan_id
#     ORDER BY s.id DESC
#     """)
#     rows = cur.fetchall()
#     conn.close()
#     return rows

def kendaraan_obj(tipe, id_, plat, merk, tarif):
     # Factory sederhana:
     # memilih class yang tepat berdasarkan tipe dari database
    if tipe == "MOBIL":
        return Mobil(id_, plat, merk, tarif)
    return Motor(id_, plat, merk, tarif)

# ---------- GUI ----------
def show_login(root_window):
    root_window.withdraw()

    login = tk.Toplevel()
    login.title("Login Admin")
    login.geometry("350x200")
    login.resizable(False, False)
    login.grab_set()

    user_var = tk.StringVar()
    pass_var = tk.StringVar()

    ttk.Label(login, text="LOGIN ADMIN", font=("Segoe UI", 12, "bold")).pack(pady=10)

    form = ttk.Frame(login)
    form.pack(pady=5, padx=15, fill="x")

    ttk.Label(form, text="Username").grid(row=0, column=0, pady=5, sticky="w")
    ttk.Entry(form, textvariable=user_var).grid(row=0, column=1, pady=5, sticky="ew")

    ttk.Label(form, text="Password").grid(row=1, column=0, pady=5, sticky="w")
    ttk.Entry(form, textvariable=pass_var, show="*").grid(row=1, column=1, pady=5, sticky="ew")

    form.columnconfigure(1, weight=1)

    def do_login():
        u = user_var.get().strip()
        p = pass_var.get().strip()

        if not u or not p:
            messagebox.showwarning("Validasi", "Username & password wajib diisi")
            return

        if dao.admin_login(u, p):
            login.destroy()
            root_window.deiconify()
        else:
            messagebox.showerror("Login gagal", "Username atau password salah")

    def on_close():
        root_window.destroy()

    btn = ttk.Button(login, text="Login", command=do_login)
    btn.pack(pady=10)

    login.protocol("WM_DELETE_WINDOW", on_close)

root = tk.Tk()
root.title("Aplikasi Penyewaan Kendaraan (Tkinter + SQLite)")
root.geometry("980x600")

show_login(root)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# =========================
# TAB 1: KENDARAAN (CRUD)
# =========================
tab_k = ttk.Frame(notebook)
notebook.add(tab_k, text="Kendaraan")

frame_k_form = ttk.LabelFrame(tab_k, text="Form Kendaraan")
frame_k_form.pack(fill="x", padx=10, pady=10)

k_id_var = tk.StringVar(value="")
k_tipe_var = tk.StringVar(value="MOBIL")
k_plat_var = tk.StringVar()
k_merk_var = tk.StringVar()
k_tarif_var = tk.StringVar()

ttk.Label(frame_k_form, text="Tipe").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Combobox(frame_k_form, textvariable=k_tipe_var, values=["MOBIL", "MOTOR"], state="readonly", width=20)\
    .grid(row=0, column=1, padx=5, pady=5, sticky="w")

ttk.Label(frame_k_form, text="Plat").grid(row=0, column=2, padx=5, pady=5, sticky="w")
ttk.Entry(frame_k_form, textvariable=k_plat_var, width=25).grid(row=0, column=3, padx=5, pady=5, sticky="w")

ttk.Label(frame_k_form, text="Merk").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(frame_k_form, textvariable=k_merk_var, width=25).grid(row=1, column=1, padx=5, pady=5, sticky="w")

ttk.Label(frame_k_form, text="Tarif/Hari").grid(row=1, column=2, padx=5, pady=5, sticky="w")
ttk.Entry(frame_k_form, textvariable=k_tarif_var, width=25).grid(row=1, column=3, padx=5, pady=5, sticky="w")

frame_k_table = ttk.Frame(tab_k)
frame_k_table.pack(fill="both", expand=True, padx=10, pady=10)

k_tree = ttk.Treeview(frame_k_table, columns=("id", "tipe", "plat", "merk", "tarif"), show="headings", height=12)
for col, txt, w in [("id","ID",60),("tipe","Tipe",90),("plat","Plat",120),("merk","Merk",180),("tarif","Tarif/Hari",120)]:
    k_tree.heading(col, text=txt)
    k_tree.column(col, width=w, anchor="w")
k_tree.pack(side="left", fill="both", expand=True)

k_scroll = ttk.Scrollbar(frame_k_table, orient="vertical", command=k_tree.yview)
k_tree.configure(yscrollcommand=k_scroll.set)
k_scroll.pack(side="right", fill="y")

# def k_refresh():
#     for i in k_tree.get_children():
#         k_tree.delete(i)
#     for row in fetch_all_kendaraan():
#         k_tree.insert("", "end", values=row)

# def k_clear():
#     k_id_var.set("")
#     k_tipe_var.set("MOBIL")
#     k_plat_var.set("")
#     k_merk_var.set("")
#     k_tarif_var.set("")

# def k_add():
#     try:
#         tipe = k_tipe_var.get().strip()
#         plat = k_plat_var.get().strip()
#         merk = k_merk_var.get().strip()
#         tarif = int(k_tarif_var.get().strip())

#         if not plat or not merk:
#             raise ValueError("Plat dan Merk wajib diisi.")
#         if tarif <= 0:
#             raise ValueError("Tarif harus > 0.")

#         dao.kendaraan_insert(tipe, plat, merk, tarif)

#         k_refresh()
#         k_clear()
#         s_reload_combo()  # auto update combobox transaksi
#         messagebox.showinfo("Sukses", "Kendaraan berhasil ditambahkan.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))


# def k_add():
#     try:
#         tipe = k_tipe_var.get().strip()
#         plat = k_plat_var.get().strip()
#         merk = k_merk_var.get().strip()
#         tarif = int(k_tarif_var.get().strip())
#         if not plat or not merk:
#             raise ValueError("Plat dan Merk wajib diisi.")
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO kendaraan(tipe, plat, merk, tarif) VALUES(?,?,?,?)", (tipe, plat, merk, tarif))
#         conn.commit()
#         conn.close()
#         k_refresh()
#         k_clear()
#         messagebox.showinfo("Sukses", "Kendaraan berhasil ditambahkan.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

def k_update():
    if not k_id_var.get():
        messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
        return
    try:
        id_ = int(k_id_var.get())
        tipe = k_tipe_var.get().strip()
        plat = k_plat_var.get().strip()
        merk = k_merk_var.get().strip()
        tarif = int(k_tarif_var.get().strip())

        if not plat or not merk:
            raise ValueError("Plat dan Merk wajib diisi.")
        if tarif <= 0:
            raise ValueError("Tarif harus > 0.")

        dao.kendaraan_update(id_, tipe, plat, merk, tarif)

        k_refresh()
        k_clear()
        s_reload_combo()
        messagebox.showinfo("Sukses", "Kendaraan berhasil diubah.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# def k_update():
#     if not k_id_var.get():
#         messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
#         return
#     try:
#         id_ = int(k_id_var.get())
#         tipe = k_tipe_var.get().strip()
#         plat = k_plat_var.get().strip()
#         merk = k_merk_var.get().strip()
#         tarif = int(k_tarif_var.get().strip())
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute("UPDATE kendaraan SET tipe=?, plat=?, merk=?, tarif=? WHERE id=?", (tipe, plat, merk, tarif, id_))
#         conn.commit()
#         conn.close()
#         k_refresh()
#         k_clear()
#         messagebox.showinfo("Sukses", "Kendaraan berhasil diubah.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

def k_delete():
    if not k_id_var.get():
        messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
        return
    if messagebox.askyesno("Konfirmasi", "Yakin hapus kendaraan ini?"):
        try:
            id_ = int(k_id_var.get())
            dao.kendaraan_delete(id_)
            k_refresh()
            k_clear()
            s_reload_combo()
            messagebox.showinfo("Sukses", "Kendaraan berhasil dihapus.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# def k_delete():
#     if not k_id_var.get():
#         messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
#         return
#     if messagebox.askyesno("Konfirmasi", "Yakin hapus kendaraan ini?"):
#         try:
#             id_ = int(k_id_var.get())
#             conn = connect()
#             cur = conn.cursor()
#             cur.execute("DELETE FROM kendaraan WHERE id=?", (id_,))
#             conn.commit()
#             conn.close()
#             k_refresh()
#             k_clear()
#             messagebox.showinfo("Sukses", "Kendaraan berhasil dihapus.")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))

def k_on_select(event):
    sel = k_tree.selection()
    if not sel:
        return
    vals = k_tree.item(sel[0], "values")
    k_id_var.set(vals[0])
    k_tipe_var.set(vals[1])
    k_plat_var.set(vals[2])
    k_merk_var.set(vals[3])
    k_tarif_var.set(vals[4])

k_tree.bind("<<TreeviewSelect>>", k_on_select)

frame_k_btn = ttk.Frame(tab_k)
frame_k_btn.pack(fill="x", padx=10, pady=(0,10))
ttk.Button(frame_k_btn, text="Tambah", command=k_add).pack(side="left", padx=5)
ttk.Button(frame_k_btn, text="Ubah", command=k_update).pack(side="left", padx=5)
ttk.Button(frame_k_btn, text="Hapus", command=k_delete).pack(side="left", padx=5)
ttk.Button(frame_k_btn, text="Clear", command=k_clear).pack(side="left", padx=5)

# =========================
# TAB 2: PELANGGAN (CRUD)
# =========================
tab_p = ttk.Frame(notebook)
notebook.add(tab_p, text="Pelanggan")

frame_p_form = ttk.LabelFrame(tab_p, text="Form Pelanggan")
frame_p_form.pack(fill="x", padx=10, pady=10)

p_id_var = tk.StringVar(value="")
p_nama_var = tk.StringVar()
p_telp_var = tk.StringVar()

ttk.Label(frame_p_form, text="Nama").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Entry(frame_p_form, textvariable=p_nama_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="w")

ttk.Label(frame_p_form, text="Telp").grid(row=0, column=2, padx=5, pady=5, sticky="w")
ttk.Entry(frame_p_form, textvariable=p_telp_var, width=30).grid(row=0, column=3, padx=5, pady=5, sticky="w")

frame_p_table = ttk.Frame(tab_p)
frame_p_table.pack(fill="both", expand=True, padx=10, pady=10)

p_tree = ttk.Treeview(frame_p_table, columns=("id","nama","telp"), show="headings", height=12)
for col, txt, w in [("id","ID",60),("nama","Nama",260),("telp","Telp",180)]:
    p_tree.heading(col, text=txt)
    p_tree.column(col, width=w, anchor="w")
p_tree.pack(side="left", fill="both", expand=True)

p_scroll = ttk.Scrollbar(frame_p_table, orient="vertical", command=p_tree.yview)
p_tree.configure(yscrollcommand=p_scroll.set)
p_scroll.pack(side="right", fill="y")

def p_refresh():
    for i in p_tree.get_children():
        p_tree.delete(i)
    for row in fetch_all_pelanggan():
        p_tree.insert("", "end", values=row)

def p_clear():
    p_id_var.set("")
    p_nama_var.set("")
    p_telp_var.set("")

def p_add():
    try:
        nama = p_nama_var.get().strip()
        telp = p_telp_var.get().strip()
        if not nama or not telp:
            raise ValueError("Nama dan Telp wajib diisi.")
        if not telp.isdigit():
            raise ValueError("Telp harus angka saja.")

        dao.pelanggan_insert(nama, telp)

        p_refresh()
        p_clear()
        s_reload_combo()
        messagebox.showinfo("Sukses", "Pelanggan berhasil ditambahkan.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# def p_add():
#     try:
#         nama = p_nama_var.get().strip()
#         telp = p_telp_var.get().strip()
#         if not nama or not telp:
#             raise ValueError("Nama dan Telp wajib diisi.")
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO pelanggan(nama, telp) VALUES(?,?)", (nama, telp))
#         conn.commit()
#         conn.close()
#         p_refresh()
#         p_clear()
#         messagebox.showinfo("Sukses", "Pelanggan berhasil ditambahkan.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))


def p_update():
    if not p_id_var.get():
        messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
        return
    try:
        id_ = int(p_id_var.get())
        nama = p_nama_var.get().strip()
        telp = p_telp_var.get().strip()
        if not nama or not telp:
            raise ValueError("Nama dan Telp wajib diisi.")
        if not telp.isdigit():
            raise ValueError("Telp harus angka saja.")

        dao.pelanggan_update(id_, nama, telp)

        p_refresh()
        p_clear()
        s_reload_combo()
        messagebox.showinfo("Sukses", "Pelanggan berhasil diubah.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# def p_update():
#     if not p_id_var.get():
#         messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
#         return
#     try:
#         id_ = int(p_id_var.get())
#         nama = p_nama_var.get().strip()
#         telp = p_telp_var.get().strip()
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute("UPDATE pelanggan SET nama=?, telp=? WHERE id=?", (nama, telp, id_))
#         conn.commit()
#         conn.close()
#         p_refresh()
#         p_clear()
#         messagebox.showinfo("Sukses", "Pelanggan berhasil diubah.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))


def p_delete():
    if not p_id_var.get():
        messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
        return
    if messagebox.askyesno("Konfirmasi", "Yakin hapus pelanggan ini?"):
        try:
            id_ = int(p_id_var.get())
            dao.pelanggan_delete(id_)
            p_refresh()
            p_clear()
            s_reload_combo()
            messagebox.showinfo("Sukses", "Pelanggan berhasil dihapus.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# def p_delete():
#     if not p_id_var.get():
#         messagebox.showwarning("Pilih data", "Klik data di tabel dulu.")
#         return
#     if messagebox.askyesno("Konfirmasi", "Yakin hapus pelanggan ini?"):
#         try:
#             id_ = int(p_id_var.get())
#             conn = connect()
#             cur = conn.cursor()
#             cur.execute("DELETE FROM pelanggan WHERE id=?", (id_,))
#             conn.commit()
#             conn.close()
#             p_refresh()
#             p_clear()
#             messagebox.showinfo("Sukses", "Pelanggan berhasil dihapus.")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))

def p_on_select(event):
    sel = p_tree.selection()
    if not sel:
        return
    vals = p_tree.item(sel[0], "values")
    p_id_var.set(vals[0])
    p_nama_var.set(vals[1])
    p_telp_var.set(vals[2])

p_tree.bind("<<TreeviewSelect>>", p_on_select)

frame_p_btn = ttk.Frame(tab_p)
frame_p_btn.pack(fill="x", padx=10, pady=(0,10))
ttk.Button(frame_p_btn, text="Tambah", command=p_add).pack(side="left", padx=5)
ttk.Button(frame_p_btn, text="Ubah", command=p_update).pack(side="left", padx=5)
ttk.Button(frame_p_btn, text="Hapus", command=p_delete).pack(side="left", padx=5)
ttk.Button(frame_p_btn, text="Clear", command=p_clear).pack(side="left", padx=5)

# =========================
# TAB 3: TRANSAKSI SEWA
# =========================
tab_s = ttk.Frame(notebook)
notebook.add(tab_s, text="Transaksi Sewa")

frame_s_form = ttk.LabelFrame(tab_s, text="Input Transaksi")
frame_s_form.pack(fill="x", padx=10, pady=10)

s_pelanggan_var = tk.StringVar()
s_kendaraan_var = tk.StringVar()
s_tanggal_var = tk.StringVar(value=str(date.today()))
s_durasi_var = tk.StringVar(value="1")
s_total_var = tk.StringVar(value="0")

pelanggan_map = {} # label -> (id, nama, telp)
kendaraan_map = {}  # label -> (id, tipe, plat, merk, tarif)
last_sewa_obj = None

def s_reload_combo():
    pelanggan_map.clear()
    kendaraan_map.clear()

    p_values = []
    for (pid, nama, telp) in fetch_all_pelanggan():
        label = f"{nama} | {telp}"
        pelanggan_map[label] = (pid, nama, telp)
        p_values.append(label)

    k_values = []
    for (kid, tipe, plat, merk, tarif) in fetch_all_kendaraan():
        label = f"{tipe} | {plat} | {merk} | {tarif}/hari"
        kendaraan_map[label] = (kid, tipe, plat, merk, tarif)
        k_values.append(label)

    cb_pelanggan["values"] = p_values
    cb_kendaraan["values"] = k_values
    if p_values:
        s_pelanggan_var.set(p_values[0])
    if k_values:
        s_kendaraan_var.set(k_values[0])

ttk.Label(frame_s_form, text="Pelanggan").grid(row=0, column=0, padx=5, pady=5, sticky="w")
cb_pelanggan = ttk.Combobox(frame_s_form, textvariable=s_pelanggan_var, state="readonly", width=45)
cb_pelanggan.grid(row=0, column=1, padx=5, pady=5, sticky="w")

ttk.Label(frame_s_form, text="Kendaraan").grid(row=1, column=0, padx=5, pady=5, sticky="w")
cb_kendaraan = ttk.Combobox(frame_s_form, textvariable=s_kendaraan_var, state="readonly", width=45)
cb_kendaraan.grid(row=1, column=1, padx=5, pady=5, sticky="w")

ttk.Label(frame_s_form, text="Tanggal (yyyy-mm-dd)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
ttk.Entry(frame_s_form, textvariable=s_tanggal_var, width=18).grid(row=0, column=3, padx=5, pady=5, sticky="w")

ttk.Label(frame_s_form, text="Durasi (hari)").grid(row=1, column=2, padx=5, pady=5, sticky="w")
ttk.Entry(frame_s_form, textvariable=s_durasi_var, width=18).grid(row=1, column=3, padx=5, pady=5, sticky="w")

ttk.Label(frame_s_form, text="Total (otomatis)").grid(row=2, column=2, padx=5, pady=5, sticky="w")
ttk.Label(frame_s_form, textvariable=s_total_var, font=("Segoe UI", 11, "bold")).grid(row=2, column=3, padx=5, pady=5, sticky="w")

def s_hitung():
    try:
        if not s_kendaraan_var.get():
            raise ValueError("Data kendaraan kosong. Tambah kendaraan dulu.")
        label = s_kendaraan_var.get()
        (kid, tipe, plat, merk, tarif) = kendaraan_map[label]
        durasi = int(s_durasi_var.get().strip())
        if durasi <= 0:
            raise ValueError("Durasi minimal 1 hari.")

         # Ambil pilihan kendaraan dari combobox -> buat object sesuai tipenya
         # Contoh penggunaan POLYMORPHISM secara nyata:
         # kelompok kami memanggil method yang sama yaitu (hitung_biaya),
         # tapi hasilnya berbeda tergantung object Mobil/Motor.
        k_obj = kendaraan_obj(tipe, kid, plat, merk, tarif)
        total = k_obj.hitung_biaya(durasi)   # <-- POLYMORPHISM (dynamic binding)
        s_total_var.set(str(total))
        return total, k_obj
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None, None


def s_simpan():
    global last_sewa_obj

    total, k_obj = s_hitung()
    if total is None:
        return

    try:
        if not s_pelanggan_var.get():
            raise ValueError("Data pelanggan kosong. Tambah pelanggan dulu.")

        # ambil pelanggan terpilih
        p_label = s_pelanggan_var.get()
        (pid, nama, telp) = pelanggan_map[p_label]

        # ambil kendaraan terpilih
        k_label = s_kendaraan_var.get()
        (kid, tipe, plat, merk, tarif) = kendaraan_map[k_label]

        tanggal = s_tanggal_var.get().strip()
        durasi = int(s_durasi_var.get().strip())

        # ===== OBJECT COMPOSITION =====
        from models.pelanggan import Pelanggan
        from models.sewa import Sewa

        pelanggan_obj = Pelanggan(pid, nama, telp)
        sewa_obj = Sewa(None, pelanggan_obj, k_obj, tanggal, durasi, total)

        # simpan ke DB via DAO
        dao.sewa_insert(kid, pid, tanggal, durasi, total)

        # simpan object terakhir (buat struk)
        last_sewa_obj = sewa_obj

        s_refresh()
        messagebox.showinfo("Sukses", "Transaksi berhasil disimpan.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



# def s_simpan():
#     dao.sewa_insert(kid, pid, tanggal, durasi, total)
    
#     total, k_obj = s_hitung()
#     if total is None:
#         return
#     try:
#         if not s_pelanggan_var.get():
#             raise ValueError("Data pelanggan kosong. Tambah pelanggan dulu.")

#         # ambil pelanggan terpilih
#         p_label = s_pelanggan_var.get()
#         (pid, nama, telp) = pelanggan_map[p_label]

#         # ambil kendaraan terpilih
#         k_label = s_kendaraan_var.get()
#         (kid, tipe, plat, merk, tarif) = kendaraan_map[k_label]

#         tanggal = s_tanggal_var.get().strip()
#         durasi = int(s_durasi_var.get().strip())

#         # ====== UPGRADE 1: object Sewa dipakai beneran (composition) ======
#         from models.pelanggan import Pelanggan
#         from models.sewa import Sewa

#         pelanggan_obj = Pelanggan(pid, nama, telp)
#         sewa_obj = Sewa(None, pelanggan_obj, k_obj, tanggal, durasi, total)
#         # sewa_obj bisa kamu pakai buat struk/log/presentasi (kalau mau)

#         # simpan ke database (tetap pakai id, karena tabel sewa pakai foreign key)
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO sewa(kendaraan_id, pelanggan_id, tanggal, durasi, total) VALUES(?,?,?,?,?)",
#             (kid, pid, tanggal, durasi, total)
#         )
#         conn.commit()
#         conn.close()

#         s_refresh()
#         messagebox.showinfo("Sukses", "Transaksi berhasil disimpan.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

        # global last_sewa_obj
        # last_sewa_obj = sewa_obj



# def s_simpan():
#         from models.pelanggan import Pelanggan
#         from models.sewa import Sewa

#         pelanggan_obj = Pelanggan(pid, nama, telp)
#         sewa_obj = Sewa(None, pelanggan_obj, k_obj, tanggal, durasi, total)
#         # sekarang sewa_obj ini bisa dipakai buat struk / log / presentasi


#     total, k_obj = s_hitung()
#     if total is None:
#         return
#     try:
#         if not s_pelanggan_var.get():
#             raise ValueError("Data pelanggan kosong. Tambah pelanggan dulu.")

#         p_label = s_pelanggan_var.get()
#         (pid, nama, telp) = pelanggan_map[p_label]

#         k_label = s_kendaraan_var.get()
#         (kid, tipe, plat, merk, tarif) = kendaraan_map[k_label]

#         tanggal = s_tanggal_var.get().strip()
#         durasi = int(s_durasi_var.get().strip())

#         conn = connect()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO sewa(kendaraan_id, pelanggan_id, tanggal, durasi, total) VALUES(?,?,?,?,?)",
#             (kid, pid, tanggal, durasi, total)
#         )
#         conn.commit()
#         conn.close()

#         s_refresh()
#         messagebox.showinfo("Sukses", "Transaksi berhasil disimpan.")
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

frame_s_btn = ttk.Frame(tab_s)
frame_s_btn.pack(fill="x", padx=10)
ttk.Button(frame_s_btn, text="Hitung", command=s_hitung).pack(side="left", padx=5, pady=5)
ttk.Button(frame_s_btn, text="Simpan Transaksi", command=s_simpan).pack(side="left", padx=5, pady=5)
ttk.Button(frame_s_btn, text="Reload Data (Combo)", command=lambda: (k_refresh(), p_refresh(), s_reload_combo(), s_refresh())).pack(side="left", padx=5, pady=5)

frame_s_table = ttk.Frame(tab_s)
frame_s_table.pack(fill="both", expand=True, padx=10, pady=10)

s_tree = ttk.Treeview(frame_s_table,
                      columns=("id","tanggal","durasi","total","kendaraan","pelanggan"),
                      show="headings", height=10)
for col, txt, w in [
    ("id","ID",60),
    ("tanggal","Tanggal",110),
    ("durasi","Durasi",70),
    ("total","Total",110),
    ("kendaraan","Kendaraan",260),
    ("pelanggan","Pelanggan",220),
]:
    s_tree.heading(col, text=txt)
    s_tree.column(col, width=w, anchor="w")
s_tree.pack(side="left", fill="both", expand=True)

s_scroll = ttk.Scrollbar(frame_s_table, orient="vertical", command=s_tree.yview)
s_tree.configure(yscrollcommand=s_scroll.set)
s_scroll.pack(side="right", fill="y")

def s_refresh():
    for i in s_tree.get_children():
        s_tree.delete(i)
    for (sid, tanggal, durasi, total, tipe, plat, merk, pnama, ptelp) in fetch_all_sewa():
        s_tree.insert("", "end", values=(
            sid,
            tanggal,
            durasi,
            total,
            f"{tipe} | {plat} | {merk}",
            f"{pnama} | {ptelp}"
        ))

def cetak_struk():
    global last_sewa_obj

    if last_sewa_obj is not None:
        struk = last_sewa_obj.to_struk()
        sid = last_sewa_obj.id or "-"
    else:
        sel = s_tree.selection()
        if not sel:
            messagebox.showwarning("Pilih transaksi", "Klik transaksi di tabel dulu.")
            return

        vals = s_tree.item(sel[0], "values")
        sid, tanggal, durasi, total, kendaraan, pelanggan = vals

        struk = (
            "========= STRUK SEWA KENDARAAN =========\n"
            f"ID Transaksi : {sid}\n"
            f"Tanggal      : {tanggal}\n"
            f"Pelanggan    : {pelanggan}\n"
            f"Kendaraan    : {kendaraan}\n"
            f"Durasi       : {durasi} hari\n"
            f"Total Biaya  : Rp {total}\n"
            "=======================================\n"
            "Terima kasih!\n"
        )

    # preview
    top = tk.Toplevel(root)
    top.title("Preview Struk")
    txt = tk.Text(top, width=55, height=14)
    txt.insert("1.0", struk)
    txt.config(state="disabled")
    txt.pack(padx=10, pady=10)

    def simpan_txt():
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"struk-{sid}.txt",
            filetypes=[("Text File", "*.txt")]
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(struk)
        messagebox.showinfo("Sukses", f"Struk disimpan:\n{path}")

    ttk.Button(top, text="Simpan sebagai .txt", command=simpan_txt).pack(pady=(0,10))


# def cetak_struk():
#     global last_sewa_obj
# if last_sewa_obj is not None:
#     struk = last_sewa_obj.to_struk()
# else:
#     # fallback: pakai data dari treeview (cara lama)
#     ...

#     sel = s_tree.selection()
#     if not sel:
#         messagebox.showwarning("Pilih transaksi", "Klik transaksi di tabel dulu.")
#         return

#     vals = s_tree.item(sel[0], "values")
#     sid, tanggal, durasi, total, kendaraan, pelanggan = vals

#     struk = (
#         "========= STRUK SEWA KENDARAAN =========\n"
#         f"ID Transaksi : {sid}\n"
#         f"Tanggal      : {tanggal}\n"
#         f"Pelanggan    : {pelanggan}\n"
#         f"Kendaraan    : {kendaraan}\n"
#         f"Durasi       : {durasi} hari\n"
#         f"Total Biaya  : Rp {total}\n"
#         "=======================================\n"
#         "Terima kasih!\n"
#     )

#     # tampilkan preview
#     top = tk.Toplevel(root)
#     top.title("Preview Struk")
#     txt = tk.Text(top, width=55, height=14)
#     txt.insert("1.0", struk)
#     txt.config(state="disabled")
#     txt.pack(padx=10, pady=10)

#     def simpan_txt():
#         path = filedialog.asksaveasfilename(
#             defaultextension=".txt",
#             initialfile=f"struk-{sid}.txt",
#             filetypes=[("Text File", "*.txt")]
#         )
#         if not path:
#             return
#         with open(path, "w", encoding="utf-8") as f:
#             f.write(struk)
#         messagebox.showinfo("Sukses", f"Struk disimpan:\n{path}")

#     ttk.Button(top, text="Simpan sebagai .txt", command=simpan_txt).pack(pady=(0,10))

ttk.Button(tab_s, text="Cetak Struk (pilih transaksi)", command=cetak_struk).pack(padx=10, pady=(0,10), anchor="w")

# initial load
k_refresh()
p_refresh()
s_reload_combo()
s_refresh()

root.mainloop()
