# class Sewa:
#     def __init__(self, id_, kendaraan_id, pelanggan_id, tanggal, durasi, total):
#         self.id = id_
#         self.kendaraan_id = kendaraan_id
#         self.pelanggan_id = pelanggan_id
#         self.tanggal = tanggal
#         self.durasi = durasi
#         self.total = total




class Sewa:
    def __init__(self, id_, pelanggan, kendaraan, tanggal, durasi, total):
        self.id = id_
        self.pelanggan = pelanggan
        self.kendaraan = kendaraan
        self.tanggal = tanggal
        self.durasi = durasi
        self.total = total

       def to_struk(self) -> str:
        return (
            "========= STRUK SEWA KENDARAAN =========\n"
            f"ID Transaksi : {self.id}\n"
            f"Tanggal      : {self.tanggal}\n"
            f"Pelanggan    : {self.pelanggan.nama} | {self.pelanggan.telp}\n"
            f"Kendaraan    : {self.kendaraan.tipe()} | {self.kendaraan.plat} | {self.kendaraan.merk}\n"
            f"Durasi       : {self.durasi} hari\n"
            f"Total Biaya  : Rp {self.total}\n"
            "=======================================\n"
       
     "Terima kasih!\n"
        )




# class Sewa:
#     def __init__(self, id_, pelanggan, kendaraan, tanggal, durasi, total):
#         # COMPOSITION/AGGREGATION:
#         # Sewa menyimpan referensi object Pelanggan dan Kendaraan
#         self.id = id_
#         self.pelanggan = pelanggan
#         self.kendaraan = kendaraan
#         self.tanggal = tanggal
#         self.durasi = durasi
#         self.total = total

#     def __str__(self):
#         return f"Sewa({self.id}) {self.pelanggan.nama} - {self.kendaraan.merk} {self.kendaraan.plat}"
