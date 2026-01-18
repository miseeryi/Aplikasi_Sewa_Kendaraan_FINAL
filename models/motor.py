from models.kendaraan import Kendaraan

class Motor(Kendaraan):
    def tipe(self) -> str:
        return "MOTOR"

    # def hitung_biaya(self, durasi_hari: int) -> int:
    #     total = self.tarif * durasi_hari
    #     if durasi_hari >= 7:
    #         total = int(total * 0.95)  # diskon 5%
    #     return total


#alfa