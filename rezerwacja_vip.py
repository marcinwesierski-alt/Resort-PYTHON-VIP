from datetime import datetime
from gosc_vip import Gosc
from pokoj_vip import Pokoj
import json


class Rezerwacja:

    def __init__(self, nazwa_hotelu, liczba_pokoi):
        self.nazwa = nazwa_hotelu
        self.pokoje = [Pokoj(nr) for nr in range(1, liczba_pokoi + 1)]

    # -------------------------
    # 🔥 ZAPIS DO PLIKU
    # -------------------------
    def zapisz_do_pliku(self):

        dane = []

        for pokoj in self.pokoje:
            for rez in pokoj.rezerwacje:
                dane.append({
                    "pokoj": pokoj.numer,
                    "gosc": str(rez["gosc"]),
                    "data_od": rez["data_od"].strftime("%Y-%m-%d"),
                    "data_do": rez["data_do"].strftime("%Y-%m-%d"),
                    "posilki": rez.get("posilki", False),
                    "numer_rezerwacji": rez.get("numer_rezerwacji", "")
                })

        with open("hotel.json", "w", encoding="utf-8") as f:
            json.dump(dane, f, indent=4, ensure_ascii=False)

        print("💾 Dane zapisane.")

    # -------------------------
    # 🔥 SPRAWDZENIE WYŁĄCZENIA
    # -------------------------
    def czy_wylaczony(self, numer, data_od, data_do):

        try:
            with open("wylaczone.json", "r", encoding="utf-8") as f:
                blokady = json.load(f)
        except:
            return False

        for b in blokady:
            if b["pokoj"] == numer:
                od = datetime.strptime(b["data_od"], "%Y-%m-%d")
                do = datetime.strptime(b["data_do"], "%Y-%m-%d")

                if not (data_do <= od or data_od >= do):
                    return True

        return False

    # -------------------------
    # 📊 STATUS (NOWA LOGIKA 🔥)
    # -------------------------
    def pokaz_stan(self):

        dzis = datetime.today()

        RED = "\033[91m"
        GREEN = "\033[92m"
        ORANGE = "\033[93m"
        PURPLE = "\033[95m"
        RESET = "\033[0m"

        print(f"\n--- STAN HOTELU: {self.nazwa} ---\n")
        gosc_max = len("Gość")
        nr_rez_max = len("Nr rez.")

        for pokoj in self.pokoje:
            for rez in pokoj.rezerwacje:

                if len(str(rez["gosc"])) > gosc_max:
                    gosc_max = len(str(rez["gosc"]))

                nr_rez = str(rez.get("numer_rezerwacji", ""))

                if len(nr_rez) > nr_rez_max:
                    nr_rez_max = len(nr_rez)

        w_gosc = gosc_max
        w_nr_rez = nr_rez_max
        w_pokoj = 6
        w_status = 20
        w_data = 10
        w_posilki = 8
        w_uslugi = 8
        w_cena = 10

        print(
                f"{'Pokój':<{w_pokoj}} | {'Nr rez.':<{w_nr_rez}} | {'Status':<{w_status}} | {'Gość':<{w_gosc}} | "
                f"{'Od':<{w_data}} | {'Do':<{w_data}} | {'Posiłki':<{w_posilki}} | "
                f"{'Usługi':<{w_uslugi}} | {'Cena':<{w_cena}}"
            )
        print("-" * 110)

        # 🔥 wczytaj wszystkie wyłączenia
        try:
            with open("wylaczone.json", "r", encoding="utf-8") as f:
                blokady = json.load(f)
        except:
            blokady = []

        for pokoj in self.pokoje:

            pokazano = False

            # ==========================
            # 🔥 REZERWACJE
            # ==========================
            for rez in pokoj.rezerwacje:

                data_od = rez["data_od"]
                data_do = rez["data_do"]

                if data_do < dzis:
                    continue

                if data_od <= dzis <= data_do:
                    status_txt = "ZAJĘTY"
                    kolor = RED
                else:
                    status_txt = "REZERWACJA"
                    kolor = ORANGE

                status_txt = status_txt.ljust(w_status)
                status = f"{kolor}{status_txt}{RESET}"

                nr_rez = str(rez.get("numer_rezerwacji", "")).ljust(w_nr_rez)
                gosc = str(rez["gosc"]).ljust(w_gosc)
                data_od_str = str(data_od.date()).ljust(w_data)
                data_do_str = str(data_do.date()).ljust(w_data)

                posilki = ("TAK" if rez.get("posilki") else "NIE").ljust(w_posilki)
                uslugi = str(rez.get("uslugi", 0)).ljust(w_uslugi)

                try:
                    cena_val = pokoj.koszt_pobytu(data_od, data_do)
                    cena = str(cena_val).ljust(w_cena)
                except:
                    cena = "-".ljust(w_cena)

                print(
                        f"{str(pokoj.numer).ljust(w_pokoj)} | {nr_rez} | {status} | {gosc} | "
                        f"{data_od_str} | {data_do_str} | {posilki} | {uslugi} | {cena}"
                    )

                pokazano = True

            # ==========================
            # 🔥 WYŁĄCZENIA
            # ==========================
            for b in blokady:

                if b["pokoj"] != pokoj.numer:
                    continue

                data_od = datetime.strptime(b["data_od"], "%Y-%m-%d")
                data_do = datetime.strptime(b["data_do"], "%Y-%m-%d")

                if data_do < dzis:
                    continue

                status_txt = "WYŁĄCZONY".ljust(w_status)
                status = f"{PURPLE}{status_txt}{RESET}"

                print(
                    f"{str(pokoj.numer).ljust(w_pokoj)} | {'-'.ljust(w_nr_rez)} | {status} | "
                    f"{'-'.ljust(w_gosc)} | "
                    f"{str(data_od.date()).ljust(w_data)} | {str(data_do.date()).ljust(w_data)} | "
                    f"{'-'.ljust(w_posilki)} | {'-'.ljust(w_uslugi)} | {'-'.ljust(w_cena)}"
                )

                pokazano = True

            # ==========================
            # 🔥 BRAK DANYCH
            # ==========================
            if not pokazano:
                status_txt = "WOLNY".ljust(w_status)
                status = f"{GREEN}{status_txt}{RESET}"

                print(
                    f"{str(pokoj.numer).ljust(w_pokoj)} | {'-'.ljust(w_nr_rez)} | {status} | "
                    f"{'-'.ljust(w_gosc)} | "
                    f"{'-'.ljust(w_data)} | {'-'.ljust(w_data)} | "
                    f"{'-'.ljust(w_posilki)} | {'-'.ljust(w_uslugi)} | {'-'.ljust(w_cena)}"
                )

            print("-" * 110)

    # -------------------------
    # ➕ MELDUJ
    # -------------------------
    def melduj(self, numer, imie, nazwisko, data_od, data_do):

        if data_od >= data_do:
            print("❌ Data końcowa musi być późniejsza niż początkowa.")
            return False

        if self.czy_wylaczony(numer, data_od, data_do):
            print("❌ Pokój wyłączony w tym terminie.")
            return False

        pokoj = self.pokoje[numer - 1]

        if not pokoj.czy_dostepny(data_od, data_do):
            print("❌ Pokój zajęty w tym terminie.")
            return False

        gosc = Gosc(imie, nazwisko)

        for rez in pokoj.rezerwacje:
            if (
                str(rez["gosc"]) == str(gosc)
                and rez["data_od"] == data_od
                and rez["data_do"] == data_do
            ):
                print("❌ Taka rezerwacja już istnieje.")
                return False

        licznik = 1

        for p in self.pokoje:
            for r in p.rezerwacje:

                nr_rez = r.get("numer_rezerwacji", "")

                if "/" in nr_rez:
                    try:
                        nr_glowny = int(nr_rez.split("/")[0])

                        if nr_glowny >= licznik:
                            licznik = nr_glowny + 1

                    except:
                        pass

        numer_rezerwacji = f"{licznik}/{numer}"

        while True:
            wybor = input("Czy posiłki? (T/N): ").strip().upper()

            if wybor == "T":
                posilki = True
                break
            elif wybor == "N":
                posilki = False
                break
            else:
                print("❌ Wpisz T/N")

        pokoj.rezerwacje.append({
            "gosc": gosc,
            "data_od": data_od,
            "data_do": data_do,
            "posilki": posilki,
            "uslugi": 0,
            "numer_rezerwacji": numer_rezerwacji
        })

        print("✅ Rezerwacja dodana.")
        return True

    # -------------------------
    # 📄 WCZYTYWANIE
    # -------------------------
    def wczytaj_z_pliku(self):
        for pokoj in self.pokoje:
            pokoj.rezerwacje.clear()
        try:
            with open("hotel.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
        except:
            return

        unikalne = set()

        for wpis in dane:

            key = (
                wpis.get("pokoj"),
                wpis.get("gosc"),
                wpis.get("data_od"),
                wpis.get("data_do")
            )

            if key in unikalne:
                continue

            unikalne.add(key)

            nr = wpis.get("pokoj")
            if nr is None:
                continue

            pokoj = self.pokoje[nr - 1]

            dane_goscia = wpis["gosc"].split()

            imie = dane_goscia[0]

            if len(dane_goscia) > 1:
                nazwisko = " ".join(dane_goscia[1:])
            else:
                nazwisko = ""

            pokoj.rezerwacje.append({
                "gosc": Gosc(imie, nazwisko),
                "data_od": datetime.strptime(wpis["data_od"], "%Y-%m-%d"),
                "data_do": datetime.strptime(wpis["data_do"], "%Y-%m-%d"),
                "posilki": wpis.get("posilki", False),
                "uslugi": 0,
                "numer_rezerwacji": wpis.get("numer_rezerwacji", "")
            })
    def przenies_do_archiwum(self):

        dzis = datetime.today()

        try:
            with open("archiwum.json", "r", encoding="utf-8") as f:
                archiwum = json.load(f)
        except:
            archiwum = []

        for pokoj in self.pokoje:

            do_usuniecia = []

            for rez in pokoj.rezerwacje:

                if rez["data_do"] < dzis:

                    nowy_wpis = {
                        "pokoj": pokoj.numer,
                        "gosc": str(rez["gosc"]),
                        "data_od": rez["data_od"].strftime("%Y-%m-%d"),
                        "data_do": rez["data_do"].strftime("%Y-%m-%d"),
                        "posilki": rez.get("posilki", False),
                        "numer_rezerwacji": rez.get("numer_rezerwacji", "")
                    }

                    if nowy_wpis not in archiwum:
                        archiwum.append(nowy_wpis)

                    do_usuniecia.append(rez)

            for rez in do_usuniecia:
                pokoj.rezerwacje.remove(rez)

        with open("archiwum.json", "w", encoding="utf-8") as f:
            json.dump(archiwum, f, indent=4, ensure_ascii=False)

        self.zapisz_do_pliku()