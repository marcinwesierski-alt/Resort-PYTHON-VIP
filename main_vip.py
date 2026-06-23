import json
from datetime import datetime
from rezerwacja_vip import Rezerwacja


def menu_rezerwacje(hotel):

    while True:

        print("\n--- REZERWACJE ---")
        print("1. Zarezerwuj")
        print("2. Zwolnij")
        print("3. Zmień")
        print("0. Powrót")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":

            try:
                numer = int(input("Numer pokoju: "))
                imie = input("Imię: ")
                nazwisko = input("Nazwisko: ")

                data_od = datetime.strptime(input("Data od (rrrr-mm-dd): "), "%Y-%m-%d")
                data_do = datetime.strptime(input("Data do (rrrr-mm-dd): "), "%Y-%m-%d")

                if hotel.melduj(numer, imie, nazwisko, data_od, data_do):
                    hotel.zapisz_do_pliku()

            except ValueError:
                print("❌ Błąd danych.")


        elif wybor == "2":

            dzis = datetime.today()
            lista = []

            print("\n--- AKTUALNE I PRZYSZŁE REZERWACJE ---")
            print()

            gosc_max = len("Gość")
            nr_rez_max = len("Nr rez.")

            for pokoj in hotel.pokoje:
                for rez in pokoj.rezerwacje:

                    if rez["data_do"] < dzis:
                        continue

                    nr_rez = str(rez.get("numer_rezerwacji", ""))

                    if len(str(rez["gosc"])) > gosc_max:
                        gosc_max = len(str(rez["gosc"]))

                    if len(nr_rez) > nr_rez_max:
                        nr_rez_max = len(nr_rez)

            w_gosc = gosc_max
            w_nr_rez = nr_rez_max

            print(
                f"{'Nr rez.':<{w_nr_rez}} | "
                f"{'Pokój':<5} | "
                f"{'Gość':<{w_gosc}} | "
                f"{'Od':<10} | "
                f"{'Do':<10}"
            )

            print("-" * (w_nr_rez + w_gosc + 36))

            for pokoj in hotel.pokoje:
                for rez in pokoj.rezerwacje:

                    if rez["data_do"] < dzis:
                        continue

                    nr_rez = str(rez.get("numer_rezerwacji", ""))

                    print(
                        f"{nr_rez:<{w_nr_rez}} | "
                        f"{pokoj.numer:<5} | "
                        f"{str(rez['gosc']):<{w_gosc}} | "
                        f"{str(rez['data_od'].date()):<10} | "
                        f"{str(rez['data_do'].date()):<10}"
                    )

                    lista.append((pokoj, rez))

            print("-" * (w_nr_rez + w_gosc + 36))

            if not lista:
                print("Brak rezerwacji.")
                continue

            print("-" * 40)

            numer = input("Podaj numer rezerwacji (0 = powrót): ").strip()

            if numer == "0":
                continue

            wybrana = None

            for pokoj, rez in lista:
                if rez.get("numer_rezerwacji", "") == numer:
                    wybrana = (pokoj, rez)
                    break

            if wybrana is None:
                print("❌ Nie znaleziono rezerwacji.")
                continue

            pokoj, rez = wybrana

            pokoj.rezerwacje.remove(rez)
            hotel.zapisz_do_pliku()

            print("✅ Rezerwacja usunięta")

        elif wybor == "3":

            dzis = datetime.today()
            lista = []

            print("\n--- AKTUALNE I PRZYSZŁE REZERWACJE ---")
            print()
            gosc_max = len("Gość")
            nr_rez_max = len("Nr rez.")

            for pokoj in hotel.pokoje:
                for rez in pokoj.rezerwacje:

                    if rez["data_do"] < dzis:
                        continue

                    nr_rez = str(rez.get("numer_rezerwacji", ""))

                    if len(str(rez["gosc"])) > gosc_max:
                        gosc_max = len(str(rez["gosc"]))

                    if len(nr_rez) > nr_rez_max:
                        nr_rez_max = len(nr_rez)

            w_gosc = gosc_max
            w_nr_rez = nr_rez_max

            print(
                f"{'Nr rez.':<{w_nr_rez}} | "
                f"{'Pokój':<5} | "
                f"{'Gość':<{w_gosc}} | "
                f"{'Od':<10} | "
                f"{'Do':<10}"
            )

            print("-" * (w_nr_rez + w_gosc + 36))

            for pokoj in hotel.pokoje:
                for rez in pokoj.rezerwacje:

                    if rez["data_do"] < dzis:
                        continue

                    nr_rez = rez.get("numer_rezerwacji", "-")

                    print(
                        f"{nr_rez:<{w_nr_rez}} | "
                        f"{pokoj.numer:<5} | "
                        f"{str(rez['gosc']):<{w_gosc}} | "
                        f"{str(rez['data_od'].date()):<10} | "
                        f"{str(rez['data_do'].date()):<10}"
                    )

                    lista.append((pokoj, rez))

            if not lista:
                print("Brak rezerwacji.")
                continue

            numer = input("\nPodaj numer rezerwacji (0 = powrót): ")

            if numer == "0":
                continue

            wybrana = None

            for pokoj, rez in lista:
                if rez.get("numer_rezerwacji", "") == numer:
                    wybrana = (pokoj, rez)
                    break

            if wybrana is None:
                print("❌ Nie znaleziono rezerwacji.")
                continue

            pokoj, rez = wybrana

            print("\n--- EDYCJA REZERWACJI ---")
            print("1. Zmień imię")
            print("2. Zmień nazwisko")
            print("3. Zmień datę od")
            print("4. Zmień datę do")
            print("5. Zmień posiłki")
            print("0. Powrót")

            opcja = input("Wybierz: ")

            if opcja == "1":

                nowe_imie = input("Nowe imię: ").strip()

                nazwisko = str(rez["gosc"]).split(maxsplit=1)

                if len(nazwisko) > 1:
                    nazwisko = nazwisko[1]
                else:
                    nazwisko = ""

                from gosc_vip import Gosc
                rez["gosc"] = Gosc(nowe_imie, nazwisko)

                hotel.zapisz_do_pliku()
                print("✅ Zmieniono imię")

            elif opcja == "2":

                nowe_nazwisko = input("Nowe nazwisko: ").strip()

                dane = str(rez["gosc"]).split(maxsplit=1)
                imie = dane[0]

                from gosc_vip import Gosc
                rez["gosc"] = Gosc(imie, nowe_nazwisko)

                hotel.zapisz_do_pliku()
                print("✅ Zmieniono nazwisko")

            elif opcja == "3":

                try:
                    nowa_data = datetime.strptime(
                        input("Nowa data od (rrrr-mm-dd): "),
                        "%Y-%m-%d"
                    )

                    rez["data_od"] = nowa_data

                    hotel.zapisz_do_pliku()
                    print("✅ Zmieniono datę od")

                except:
                    print("❌ Błędna data")

            elif opcja == "4":

                try:
                    nowa_data = datetime.strptime(
                        input("Nowa data do (rrrr-mm-dd): "),
                        "%Y-%m-%d"
                    )

                    rez["data_do"] = nowa_data

                    hotel.zapisz_do_pliku()
                    print("✅ Zmieniono datę do")

                except:
                    print("❌ Błędna data")

            elif opcja == "5":

                rez["posilki"] = not rez.get("posilki", False)

                hotel.zapisz_do_pliku()

                print(
                    f"✅ Posiłki ustawiono na "
                    f"{'TAK' if rez['posilki'] else 'NIE'}"
                )

        elif wybor == "0":
            break

        else:
            print("❌ Niepoprawna opcja.")


def menu_uslugi():

    while True:

        print("\n--- REZERWACJE POZOSTAŁE ---")
        print("1. Sale konferencyjne")
        print("2. Sale bankietowe")
        print("3. Basen")
        print("4. Korty")
        print("5. Sauna")
        print("6. Kajaki")
        print("7. Leżaki")
        print("0. Powrót")

        wybor = input("Wybierz opcję: ")

        if wybor == "0":
            break

        elif wybor == "1":
            menu_sale_konferencyjne()

        elif wybor in ["2", "3", "4", "5", "6", "7"]:
            print("W przygotowaniu")

def menu_sale_konferencyjne():

    while True:

        print("\n--- SALE KONFERENCYJNE ---")
        print("1. Lista sal")
        print("2. Ustaw pojemność sal")
        print("3. Rezerwacje")
        print("0. Powrót")

        wybor = input("Wybierz: ")

        if wybor == "0":
            break


        elif wybor == "1":

            try:

                with open("zasoby.json", "r", encoding="utf-8") as f:

                    zasoby = json.load(f)

                liczba_sal = zasoby.get("sale_konferencyjne", 0)

                print("\n--- LISTA SAL ---")

                if liczba_sal == 0:

                    print("Brak sal konferencyjnych.")

                else:

                    for i in range(1, liczba_sal + 1):
                        print(f"K{i}")


            except Exception as e:

                print("❌ Błąd:", e)

        elif wybor == "2":
            print("W przygotowaniu")

        elif wybor == "3":
            print("W przygotowaniu")

def menu_zmiana_pokoi():

    try:
        with open("zasoby.json", "r", encoding="utf-8") as f:
            zasoby = json.load(f)
    except Exception as e:
        print("❌ Błąd:", e)
        return

    try:
        print("👉 ENTER = bez zmian")

        nowe_1 = input(f"1-os ({zasoby.get('1_os', 0)}): ")
        nowe_2 = input(f"2-os ({zasoby.get('2_os', 0)}): ")
        nowe_3 = input(f"3-os ({zasoby.get('3_os', 0)}): ")
        nowe_25 = input(f"25-os ({zasoby.get('25_os', 0)}): ")

        if nowe_1.strip():
            zasoby["1_os"] = int(nowe_1)

        if nowe_2.strip():
            zasoby["2_os"] = int(nowe_2)

        if nowe_3.strip():
            zasoby["3_os"] = int(nowe_3)

        if nowe_25.strip():
            zasoby["25_os"] = int(nowe_25)

        with open("zasoby.json", "w", encoding="utf-8") as f:
            json.dump(zasoby, f, indent=4)

        print("✅ Zapisano zmiany")

    except ValueError:
        print("❌ Wpisz poprawne liczby")

def zmien_zasob(nazwa_klucza, opis):

    try:
        with open("zasoby.json", "r", encoding="utf-8") as f:
            zasoby = json.load(f)
    except Exception as e:
        print("❌ Błąd:", e)
        return

    try:

        obecna = zasoby.get(nazwa_klucza, 0)

        nowa = input(f"{opis} ({obecna}): ")

        if nowa.strip():

            zasoby[nazwa_klucza] = int(nowa)

            with open("zasoby.json", "w", encoding="utf-8") as f:
                json.dump(zasoby, f, indent=4)

            print("✅ Zapisano zmiany")

    except ValueError:
        print("❌ Wpisz poprawną liczbę")

def menu_wylaczone_pokoje():

    while True:

        blokady = []

        try:
            with open("wylaczone.json", "r", encoding="utf-8") as f:
                blokady = json.load(f)
        except:
            pass

        print("\n--- WYŁĄCZONE POKOJE ---")

        if not blokady:
            print("Brak wyłączonych pokoi.")
        else:
            for b in blokady:
                print(f"Pokój {b['pokoj']} | {b['data_od']} → {b['data_do']}")

        print("-" * 40)
        print("1. Dodaj wyłączenie")
        print("0. Powrót")

        wybor = input("Wybierz: ")

        if wybor == "1":

            numer_input = input("Podaj numer pokoju (0 = powrót): ")

            if numer_input == "0":
                continue

            try:
                numer = int(numer_input)
            except ValueError:
                print("❌ Błąd")
                continue

            data_od = input("Data od (rrrr-mm-dd): ")
            data_do = input("Data do (rrrr-mm-dd): ")

            blokady.append({
                "pokoj": numer,
                "data_od": data_od,
                "data_do": data_do
            })

            with open("wylaczone.json", "w", encoding="utf-8") as f:
                json.dump(blokady, f, indent=4)

            print("✅ Pokój wyłączony")

        elif wybor == "0":
            break

def menu_zmiany_dostepnosci():

    while True:

        print("\n--- ZMIANY DOSTĘPNOŚCI ---")
        print("1. Pokoje")
        print("2. Sale konferencyjne")
        print("3. Sale bankietowe")
        print("4. Basen")
        print("5. Korty")
        print("6. Sauna")
        print("7. Kajaki")
        print("8. Leżaki")
        print("9. Pokoje wyłączone z użytkowania")
        print("0. Powrót")

        wybor = input("Wybierz: ")

        if wybor == "0":
            break

        elif wybor == "1":
            menu_zmiana_pokoi()
        elif wybor == "9":
            menu_wylaczone_pokoje()
        elif wybor == "2":
            zmien_zasob("sale_konferencyjne", "Sale konferencyjne")

        elif wybor == "3":
            zmien_zasob("sale_bankietowe", "Sale bankietowe")

        elif wybor == "4":
            zmien_zasob("baseny", "Baseny")

        elif wybor == "5":
            zmien_zasob("korty", "Korty")

        elif wybor == "6":
            zmien_zasob("sauny", "Sauny")

        elif wybor == "7":
            zmien_zasob("kajaki", "Kajaki")

        elif wybor == "8":
            zmien_zasob("lezaki", "Leżaki")

        else:
            print("W przygotowaniu")

def menu_dostepnosc():

    try:
        with open("zasoby.json", "r", encoding="utf-8") as f:
            zasoby = json.load(f)
    except Exception as e:
        print("❌ Błąd:", e)
        return

    print("\n--- DOSTĘPNOŚĆ ---")
    print("1. Zestawienie")
    print("2. Zmiany")
    print("0. Powrót")

    wybor = input("Wybierz: ")

    if wybor == "1":

        print("\n--- ZESTAWIENIE DOSTĘPNOŚCI ---")

        print(f"Pokoje 1-osobowe: {zasoby.get('1_os', 0)}")
        print(f"Pokoje 2-osobowe: {zasoby.get('2_os', 0)}")
        print(f"Pokoje 3-osobowe: {zasoby.get('3_os', 0)}")
        print(f"Pokoje 25-osobowe: {zasoby.get('25_os', 0)}")

        print()

        print(f"Sale konferencyjne: {zasoby.get('sale_konferencyjne', 0)}")
        print(f"Sale bankietowe: {zasoby.get('sale_bankietowe', 0)}")
        print(f"Basen: {zasoby.get('baseny', 0)}")
        print(f"Korty: {zasoby.get('korty', 0)}")
        print(f"Sauna: {zasoby.get('sauny', 0)}")
        print(f"Kajaki: {zasoby.get('kajaki', 0)}")
        print(f"Leżaki: {zasoby.get('lezaki', 0)}")

    elif wybor == "2":
        menu_zmiany_dostepnosci()

        return

def menu_ustawienia(hotel):

    while True:

        print("\n--- USTAWIENIA ---")
        print("1. Dostępność")
        print("0. Powrót")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            menu_dostepnosc()

        elif wybor == "0":
            break

        else:
            print("❌ Niepoprawna opcja.")


def main():

    try:
        with open("zasoby.json", "r", encoding="utf-8") as f:
            zasoby = json.load(f)
    except Exception as e:
        print("❌ Błąd:", e)
        input("ENTER aby wyjść...")
        return

    liczba_pokoi = (
        zasoby.get("1_os", 0)
        + zasoby.get("2_os", 0)
        + zasoby.get("3_os", 0)
        + zasoby.get("25_os", 0)
    )

    hotel = Rezerwacja("Python Resort", liczba_pokoi)
    hotel.wczytaj_z_pliku()
    hotel.przenies_do_archiwum()

    while True:

        print("\n=== SYSTEM HOTELU ===")
        print("1. Status pokoi")
        print("2. Rezerwacje")
        print("3. Rezerwacje pozostałe")
        print("9. Ustawienia")
        print("0. Wyjście")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            hotel.pokaz_stan()

        elif wybor == "2":
            menu_rezerwacje(hotel)

        elif wybor == "3":
            menu_uslugi()

        elif wybor == "9":
            menu_ustawienia(hotel)

        elif wybor == "0":
            print("Zamykanie systemu...")
            break

        else:
            print("❌ Niepoprawna opcja.")


if __name__ == "__main__":
    main()