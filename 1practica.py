
import string

# Verificare prenume fără cifre
def validare_pre_nume(cuv):
    for char in cuv:
        if char.isdigit():
            print("Invalid: cifră introdusă")
            return False
        if char in string.punctuation:
            print("Invalid: caracter special introdus")
            return False
    return True

# Verificare CNP
def validare_cnp(cnp):
    if len(cnp) != 13:
        print("Invalid: lungimea CNP-ului nu corespunde")
        return False

    if not cnp.isdigit():
        print("Invalid: nu ați introdus cifre")
        return False

    if cifra_control(cnp) != int(cnp[12]):
        print("Invalid: CNP invalid")
        return False

    return True

def cifra_control(cnp):
    constanta = '279146358279'
    suma = 0

    for i in range(12):
        suma += int(cnp[i]) * int(constanta[i])

    ctrl = suma % 11
    if ctrl == 10:
        ctrl = 1

    return ctrl

def validare_date(date):
    for field in date:
        if not field.strip():  # Verifică dacă field este gol sau conține spații
            print("Invalid: date incomplete")
            return False
    return True

# Lista pentru a stoca toți cursanții
lista_cursanti = []

# Meniu principal
while True:
    print("\nMeniu Principal")
    print("1. Adaugă cursant")
    print("2. Afișează lista cursanților")
    print("3. Salvează cursanții în fișier")
    print("0. Ieșire")

    optiune = input("Alegeți o opțiune: ")

    if optiune == '1':
        # Adaugă cursant
        print("Introduceți datele cursantului:")

        # Colectare și validare prenume
        prenume = input("Prenume: ")
        while not validare_pre_nume(prenume):
            prenume = input("Prenume: ")

        # Colectare și validare nume
        nume = input("Nume: ")
        while not validare_pre_nume(nume):
            nume = input("Nume: ")

        # Colectare și validare CNP
        CNP = input("CNP: ")
        while not validare_cnp(CNP):
            CNP = input("CNP: ")

        # Crearea cursantului și validarea datelor
        cursant = {
            "prenume": prenume,
            "nume": nume,
            "CNP": CNP
        }

        if not validare_date([prenume, nume, CNP]):
            continue

        lista_cursanti.append(cursant)
        print(f"Cursantul {prenume} {nume} a fost adăugat cu succes.")

    elif optiune == '2':
        # Afișează lista cursanților
        if not lista_cursanti:
            print("Nu există cursanți în listă.")
        else:
            print("Lista finală a cursanților:")
            for i, cursant in enumerate(lista_cursanti, start=1):
                print(f"Cursantul {i}: {cursant['prenume']} {cursant['nume']} - CNP: {cursant['CNP']}")

    elif optiune == '3':
        # Salvează cursanții în fișier
        nume_fisier = "cursanti.txt"
        with open(nume_fisier, 'w') as f:
            for cursant in lista_cursanti:
                f.write(f"Prenume: {cursant['prenume']}, Nume: {cursant['nume']}, CNP: {cursant['CNP']}\n")
        print(f"Datele cursanților au fost salvate în fișierul {nume_fisier}.")

    elif optiune == '0':
        # Ieșire
        print("La revedere!")
        break

    else:
        print("Opțiune invalidă. Încercați din nou.")






