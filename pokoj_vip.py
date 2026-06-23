from datetime import datetime


class Pokoj:

    def __init__(self, numer, cena=100):

        self.numer = numer
        self.cena = cena
        self.rezerwacje = []


# ==========================================================
# DODAWANIE REZERWACJI
# ==========================================================

    def dodaj_rezerwacje(self, gosc, data_od, data_do, posilki=False):

        numer_rezerwacji = f"{self.numer}/{data_od.year}/{len(self.rezerwacje)+1}"

        self.rezerwacje.append({
            "gosc": gosc,
            "data_od": data_od,
            "data_do": data_do,
            "posilki": posilki,
            "uslugi": 0,
            "numer_rezerwacji": numer_rezerwacji
        })


# ==========================================================
# SPRAWDZANIE DOSTĘPNOŚCI
# ==========================================================

    def czy_dostepny(self, data_od, data_do):

        for rez in self.rezerwacje:

            if not (data_do <= rez["data_od"] or data_od >= rez["data_do"]):
                return False

        return True


# ==========================================================
# KOSZT POBYTU
# ==========================================================

    def koszt_pobytu(self, data_od, data_do):

        dni = (data_do - data_od).days

        return dni * self.cena