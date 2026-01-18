from models.kendaraan import Kendaraan

class Mobil(Kendaraan):
    def tipe(self) -> str:
        return "MOBIL"

    def hitung_biaya(self, durasi_hari: int) -> int:
        # contoh: mobil ada asuransi flat 10.000
        return (self.tarif * durasi_hari) + 10000


