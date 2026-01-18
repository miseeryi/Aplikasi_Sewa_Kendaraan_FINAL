from abc import ABC, abstractmethod

class Kendaraan(ABC):
    def __init__(self, id_, plat, merk, tarif):
        self.id = id_
        self.plat = plat
        self.merk = merk
        self.tarif = tarif

    @abstractmethod
    def tipe(self) -> str:
        pass

    # def hitung_biaya(self, durasi_hari: int) -> int:
    #     # default
    #     return self.tarif * durasi_hari


#alfa


