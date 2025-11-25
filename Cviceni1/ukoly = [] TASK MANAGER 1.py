ukoly = [] 

def pridat_ukol():
    while True:
        nazev = input("Zadejte název úkolu: ")
        if nazev == "":
            print("Název úkolu nesmí být prázdný. Zkuste to znovu.\n")
            print("Název úkolu nesmí být prázdný. Zkuste to znovu.\n")
            continue

        popis = input("Zadejte popis úkolu: ")
        if popis == "":
            print("Popis úkolu nesmí být prázdný. Zkuste to znovu.\n")
            continue

        ukol = {"nazev": nazev, "popis": popis}
        ukoly.append(ukol)
        print("Úkol '" + nazev + "' byl přidán.\n")
        break

def zobrazit_ukoly():
    if len(ukoly) == 0:
        print("Seznam úkolů je prázdný.\n")
    else:
        print("Seznam úkolů:")
        cislo = 1
        for ukol in ukoly: 
            print(str(cislo) + ". " + ukol["nazev"] + " - " + ukol["popis"])
            cislo = cislo + 1
        print()

def odstranit_ukol():
    if len(ukoly) == 0: 
        print("Seznam úkolů je prázdný. Není co odstraňovat.\n")
        return

    zobrazit_ukoly()

    while True:
        volba = input("Zadejte číslo úkolu, který chcete odstranit: ")
        if volba.isdigit(): 
            cislo = int(volba) 
            if cislo >= 1 and cislo <= len(ukoly):
                odebrany = ukoly.pop(cislo - 1) 
                print("Úkol '" + odebrany["nazev"] + "' byl odstraněn.\n")
                break
            else:
                print("Neplatné číslo. Zadejte číslo mezi 1 a " + str(len(ukoly)) + ".\n")
        else:
            print("Zadejte prosím platné číslo.\n")

def hlavni_menu():
    while True:
        print("Správce úkolů - Hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Odstranit úkol")
        print("4. Konec programu")
        volba = input("Vyberte možnost (1-4): ")

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            odstranit_ukol()
        elif volba == "4":
            print("Konec programu.")
            break
        else:
            print("Neplatná volba. Zkuste to znovu.\n")

hlavni_menu()