class Gosc:

    def __init__(self, imie: str, nazwisko: str):

        self.imie = imie.strip().capitalize()
        self.nazwisko = nazwisko.strip().capitalize()

    def pelne_imie(self):

        return f"{self.imie} {self.nazwisko}"

    def __repr__(self):

        return self.pelne_imie()