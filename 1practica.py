import csv
import datetime

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
    return nume, prenume, cnp


def validare_nume(nume_introdus):
    # Verificăm dacă numele introdus conține doar litere
    if not nume_introdus.isalpha():
        print("Numele trebuie să conțină doar litere.")
        return False
    return True


def validare_cnp(cnp_introdus):
    # Verificăm dacă lungimea CNP-ului introdus este de 13 caractere
    if len(cnp_introdus) != 13:
        print("Lungimea CNP-ului nu este corectă.")
        return False
    if not cnp_introdus.isdigit():
        print("CNP-ul trebuie să conțină doar cifre.")
        return False

    # Calculăm cifra de control
    constanta_control = "279146358279"
    suma = 0
    for i in range(12):
        suma += int(cnp_introdus[i]) * int(constanta_control[i])
    cifra_control_calculată = suma % 11
    if cifra_control_calculată == 10:
        cifra_control_calculată = 1

    # Verificăm cifra_control_calculată vs cifra_control din CNP
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

if __name__ == "__main__":
    lista_cursanti = []
    while True:
        print("1. Introduceți un nou cursant")
        print("2. Afișați lista cursanților")
        print("3. Ștergeți un cursant")
        print("4. Salvați datele")
        print("5. Ieșiți")

        optiune = input("Alegeți o opțiune: ")
        if optiune == "5":
            print("Programul se închide")
            break
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
