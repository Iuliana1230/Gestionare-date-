import csv
import datetime

lista_cursanti = []

def prelucrare_date_citite(data):
    if len(data) < 3:
        print("Datele introduse pentru cursant sunt incomplete")
        return False
    nume = data[0]
    if len(data) == 3:
        prenume = data[1]
        cnp = data[2]
    if len(data) == 4:
        prenume = data[1] + " " + data[2]
        cnp = data[3]

    # Verificarea unicității CNP-ului
    for cursant in lista_cursanti:
        if cursant['cnp'] == cnp:
            print(f"CNP-ul {cnp} există deja în lista cursanților.")
            return False

    return nume, prenume, cnp

def validare_nume(nume_introdus):
    if not nume_introdus.isalpha():
        print("Numele trebuie să conțină doar litere.")
        return False
    return True

def validare_cnp(cnp_introdus):
    if len(cnp_introdus) != 13:
        print("Lungimea CNP-ului nu este corectă.")
        return False
    if not cnp_introdus.isdigit():
        print("CNP-ul trebuie să conțină doar cifre.")
        return False

    constanta_control = "279146358279"
    suma = 0
    for i in range(12):
        suma += int(cnp_introdus[i]) * int(constanta_control[i])
    cifra_control_calculată = suma % 11
    if cifra_control_calculată == 10:
        cifra_control_calculată = 1

    if cifra_control_calculată != int(cnp_introdus[12]):
        print("Cifra de control a CNP-ului nu este corectă.")
        return False
    return True

def salveaza_date(format_fisier):
    global lista_cursanti
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H_%M")
    file_name = f"Lista_cursanti_{timestamp}.{format_fisier}"

    if format_fisier == "txt":
        with open(file_name, mode="w") as my_file:
            my_file.write("Nume \t Prenume \t CNP \n")
            for cursant in lista_cursanti:
                my_file.write(cursant['nume'] + "\t" + cursant['prenume'] + "\t" + cursant['cnp'] + "\n")
        print(f"Fișierul {file_name} a fost salvat cu succes.")
    elif format_fisier == "csv":
        with open(file_name, mode="w", newline='') as csv_file:
            fieldnames = ['Nume', 'Prenume', 'CNP']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for cursant in lista_cursanti:
                writer.writerow({'Nume': cursant['nume'], 'Prenume': cursant['prenume'], 'CNP': cursant['cnp']})
        print(f"Fișierul {file_name} a fost salvat cu succes.")
    else:
        print("Formatul specificat nu este suportat. Vă rugăm să alegeți între 'txt' și 'csv'.")

def sterge_inregistrare_index(index):
    global lista_cursanti
    try:
        index = int(index)
        if 0 <= index < len(lista_cursanti):
            del lista_cursanti[index]
            print(f"Inregistrarea de la indexul {index} a fost stearsa.")
        else:
            print("Indexul introdus este în afara intervalului.")
    except ValueError:
        print("Indexul introdus nu este valid.")

def sterge_inregistrare_cnp(cnp):
    global lista_cursanti
    inregistrare_gasita = False
    for cursant in lista_cursanti:
        if cursant['cnp'] == cnp:
            lista_cursanti.remove(cursant)
            inregistrare_gasita = True
            print(f"Inregistrarea cu CNP-ul {cnp} a fost stearsa.")
            break
    if not inregistrare_gasita:
        print(f"Nu s-a găsit nicio înregistrare cu CNP-ul {cnp}.")


def actualizeaza_inregistrare(id):
    global lista_cursanti
    try:
        id = int(id)
        if 0 <= id < len(lista_cursanti):
            cursant = lista_cursanti[id]
            print(f"Actualizați datele pentru cursantul cu ID-ul {id}: {cursant}")
            camp_de_actualizat = input("Ce doriți să actualizați? (nume/prenume/cnp): ").lower()

            if camp_de_actualizat not in ["nume", "prenume", "cnp"]:
                print("Câmp invalid. Vă rugăm să alegeți între 'nume', 'prenume' sau 'cnp'.")
                return

            noua_valoare = input(f"Introduceți noile date  {camp_de_actualizat}: ")

            if camp_de_actualizat == "nume":
                if not validare_nume(noua_valoare):
                    print("Numele introdus nu este valid.")
                    return
                cursant["nume"] = noua_valoare

            elif camp_de_actualizat == "prenume":
                if not validare_nume(noua_valoare.replace(" ", "")):
                    print("Prenumele introdus nu este valid.")
                    return
                cursant["prenume"] = noua_valoare

            elif camp_de_actualizat == "cnp":
                if not validare_cnp(noua_valoare):
                    return
                if any(c['cnp'] == noua_valoare for c in lista_cursanti):
                    print(f"CNP-ul {noua_valoare} există deja în lista cursanților.")
                    return
                cursant["cnp"] = noua_valoare

            print("Informațiile cursantului au fost actualizate cu succes.")
        else:
            print("ID-ul introdus este în afara intervalului.")
    except ValueError:
        print("ID-ul introdus nu este valid.")


def incarca_date_din_fisier(file_name):
    global lista_cursanti
    try:
        if file_name.endswith('.txt'):
            with open(file_name, mode='r') as file:
                next(file)  # Skip header line
                for line in file:
                    date_cursant = line.strip().split("\t")
                    if len(date_cursant) == 3:
                        nume, prenume, cnp = date_cursant
                    elif len(date_cursant) == 4:
                        nume, prenume, _, cnp = date_cursant
                    else:
                        print(f"Linia nu este formatată corect: {line}")
                        continue
                    if not any(c['cnp'] == cnp for c in lista_cursanti):
                        lista_cursanti.append({"nume": nume, "prenume": prenume, "cnp": cnp})
        elif file_name.endswith('.csv'):
            with open(file_name, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    nume = row['Nume']
                    prenume = row['Prenume']
                    cnp = row['CNP']
                    if not any(c['cnp'] == cnp for c in lista_cursanti):
                        lista_cursanti.append({"nume": nume, "prenume": prenume, "cnp": cnp})
        else:
            print("Formatul specificat nu este suportat. Vă rugăm să folosiți un fișier .txt sau .csv.")
        print(f"Datele din fișierul {file_name} au fost încărcate cu succes.")
    except FileNotFoundError:
        print(f"Fișierul {file_name} nu a fost găsit.")


def concatenare_fisiere():
    tip_fisier = input("Introduceți tipul fișierelor pentru concatenare (txt/csv): ").lower()
    if tip_fisier not in ["txt", "csv"]:
        print("Tipul de fișier introdus nu este valid. Vă rugăm să alegeți 'txt' sau 'csv'.")
        return

    fisiere = input("Introduceți numele fișierelor de concatenat separate prin spațiu: ").split()

    if not fisiere:
        print("Nu ați introdus niciun fișier.")
        return

    try:
        if tip_fisier == "txt":
            with open(f"concatenat_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}.txt", mode="w") as fisier_final:
                for nume_fisier in fisiere:
                    with open(nume_fisier, mode="r") as fisier:
                        continut = fisier.read()
                        fisier_final.write(continut)
                        fisier_final.write("\n")
        elif tip_fisier == "csv":
            with open(f"concatenat_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}.csv", mode="w",
                      newline='') as fisier_final:
                writer = csv.writer(fisier_final)
                header_written = False
                for nume_fisier in fisiere:
                    with open(nume_fisier, mode="r", newline='') as fisier:
                        reader = csv.reader(fisier)
                        header = next(reader)
                        if not header_written:
                            writer.writerow(header)
                            header_written = True
                        for row in reader:
                            writer.writerow(row)
        print(
            f"Fișierele au fost concatenate cu succes în fișierul 'concatenat_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}.{tip_fisier}'.")
    except FileNotFoundError:
        print(
            "Unul sau mai multe fișiere nu au fost găsite. Vă rugăm să verificați numele fișierelor și să încercați din nou.")
    except Exception as e:
        print(f"A apărut o eroare: {e}")


if __name__ == "__main__":

    while True:
        print("1. Introduceți un nou cursant")
        print("2. Afișați lista cursanților")
        print("3. Ștergeți un cursant")
        print("4. Salvați datele")
        print("5. Încărcați datele dintr-un fișier")
        print("6. Actualizați datele unui cursant")
        print("7. Concatenare fișiere TXT/CSV")
        print("8. Ieșiți")

        optiune = input("Alegeți o opțiune: ")
        if optiune == "8":
            print("Programul se închide")
            break
        if optiune == "7":
            concatenare_fisiere()
            continue
        if optiune == "6":
            id_actualizare = input("Introduceți ID-ul cursantului pe care doriți să-l actualizați: ")
            actualizeaza_inregistrare(id_actualizare)
            continue
        if optiune == "5":
            file_name = input("Introduceți numele fișierului din care doriți să încărcați datele: ")
            # Apel funcție încărcare date din fișier, funcție neprezentată aici
            continue
        if optiune == "4":
            format_fisier = input("În ce format doriți salvarea datelor? txt/csv? ").lower()
            salveaza_date(format_fisier)
            continue
        if optiune == "3":
            sub_optiune = input("Doriți să ștergeți pe baza de index sau CNP? (index/cnp): ").lower()
            if sub_optiune == "index":
                index_stergere = input("Introduceți indexul cursantului de șters: ")
                sterge_inregistrare_index(index_stergere)
            elif sub_optiune == "cnp":
                cnp_stergere = input("Introduceți CNP-ul cursantului de șters: ")
                sterge_inregistrare_cnp(cnp_stergere)
            else:
                print("Opțiune invalidă. Vă rugăm să alegeți din nou.")
            continue
        if optiune == "2":
            for i, cursant in enumerate(lista_cursanti):
                print(f"{i}: Nume: {cursant['nume']}, Prenume: {cursant['prenume']}, CNP: {cursant['cnp']}")
            continue
        if optiune == "1":
            new_line = input("Introduceți noul cursant: ")
            date_cursant = new_line.split()
            rezultat = prelucrare_date_citite(date_cursant)
            if not rezultat:
                continue
            nume = rezultat[0]
            prenume = rezultat[1]
            cnp = rezultat[2]
            if not validare_cnp(cnp):
                continue
            if not validare_nume(nume):
                print("Numele introdus nu este valid.")
                continue
            if not validare_nume(prenume.replace(" ", "")):
                print("Prenumele introdus nu este valid.")
                continue
            dict_cursant = {"nume": nume, "prenume": prenume, "cnp": cnp}
            lista_cursanti.append(dict_cursant)
            print("Cursant adăugat cu succes.")
        else:
            print("Opțiune invalidă. Vă rugăm să alegeți din nou.")
