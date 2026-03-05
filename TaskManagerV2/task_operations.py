from database import Ukol
from datetime import datetime


def pridat_ukol(session):
    print("\n=== Přidání nového úkolu ===")

    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if nazev:
            break
        print("⚠ Název úkolu nesmí být prázdný! Zkuste to znovu.")

    while True:
        popis = input("Zadejte popis úkolu: ").strip()
        if popis:
            break
        print("⚠ Popis úkolu nesmí být prázdný! Zkuste to znovu.")

    try:
        novy_ukol = Ukol(
            nazev=nazev,
            popis=popis,
            stav='Nezahájeno',
            datum_vytvoreni=datetime.now()
        )
        session.add(novy_ukol)
        session.commit()
        print(f"✓ Úkol '{nazev}' byl úspěšně přidán!")
        return True
    except Exception as e:
        session.rollback()
        print(f"✗ Chyba při přidávání úkolu: {e}")
        return False


def zobrazit_ukoly(session):
    print("\n=== Seznam úkolů ===")
    try:
        ukoly = session.query(Ukol).filter(
            Ukol.stav.in_(['Nezahájeno', 'Probíhá'])
        ).all()

        if not ukoly:
            print("📋 Seznam úkolů je prázdný.")
            return

        print(f"\n{'ID':<5} {'Název':<30} {'Stav':<15} {'Popis':<40}")
        print("-" * 90)

        for ukol in ukoly:
            nazev_zkraceny = ukol.nazev[:27] + "..." if len(ukol.nazev) > 30 else ukol.nazev
            popis_zkraceny = ukol.popis[:37] + "..." if len(ukol.popis) > 40 else ukol.popis
            print(f"{ukol.id:<5} {nazev_zkraceny:<30} {ukol.stav:<15} {popis_zkraceny:<40}")

        print()
    except Exception as e:
        print(f"✗ Chyba při zobrazování úkolů: {e}")


def aktualizovat_ukol(session):
    print("\n=== Aktualizace úkolu ===")
    try:
        ukoly = session.query(Ukol).filter(
            Ukol.stav.in_(['Nezahájeno', 'Probíhá'])
        ).all()

        if not ukoly:
            print("📋 Nejsou žádné úkoly k aktualizaci.")
            return False

        print(f"\n{'ID':<5} {'Název':<30} {'Aktuální stav':<15}")
        print("-" * 50)
        for ukol in ukoly:
            nazev_zkraceny = ukol.nazev[:27] + "..." if len(ukol.nazev) > 30 else ukol.nazev
            print(f"{ukol.id:<5} {nazev_zkraceny:<30} {ukol.stav:<15}")
        while True:
            try:
                ukol_id = int(input("\nZadejte ID úkolu, který chcete aktualizovat: "))
                ukol = session.query(Ukol).filter_by(id=ukol_id).first()

                if ukol and ukol.stav in ['Nezahájeno', 'Probíhá']:
                    break
                else:
                    print("⚠ Úkol s tímto ID neexistuje nebo již byl dokončen. Zkuste to znovu.")
            except ValueError:
                print("⚠ Neplatné ID! Zadejte prosím číslo.")
        print("\nVyberte nový stav:")
        print("1. Probíhá")
        print("2. Hotovo")

        while True:
            volba = input("Vaše volba (1-2): ").strip()
            if volba == '1':
                novy_stav = 'Probíhá'
                break
            elif volba == '2':
                novy_stav = 'Hotovo'
                break
            else:
                print("⚠ Neplatná volba! Zadejte 1 nebo 2.")

        ukol.stav = novy_stav
        session.commit()
        print(f"✓ Stav úkolu '{ukol.nazev}' byl změněn na '{novy_stav}'!")
        return True

    except Exception as e:
        session.rollback()
        print(f"✗ Chyba při aktualizaci úkolu: {e}")
        return False


def odstranit_ukol(session):
    print("\n=== Odstranění úkolu ===")
    try:
        ukoly = session.query(Ukol).all()

        if not ukoly:
            print("📋 Nejsou žádné úkoly k odstranění.")
            return False

        print(f"\n{'ID':<5} {'Název':<30} {'Stav':<15}")
        print("-" * 50)
        for ukol in ukoly:
            nazev_zkraceny = ukol.nazev[:27] + "..." if len(ukol.nazev) > 30 else ukol.nazev
            print(f"{ukol.id:<5} {nazev_zkraceny:<30} {ukol.stav:<15}")
        while True:
            try:
                ukol_id = int(input("\nZadejte ID úkolu, který chcete odstranit: "))
                ukol = session.query(Ukol).filter_by(id=ukol_id).first()

                if ukol:
                    break
                else:
                    print("⚠ Úkol s tímto ID neexistuje. Zkuste to znovu.")
            except ValueError:
                print("⚠ Neplatné ID! Zadejte prosím číslo.")
        potvrzeni = input(f"Opravdu chcete odstranit úkol '{ukol.nazev}'? (ano/ne): ").strip().lower()

        if potvrzeni in ['ano', 'a', 'yes', 'y']:
            session.delete(ukol)
            session.commit()
            print(f"✓ Úkol '{ukol.nazev}' byl úspěšně odstraněn!")
            return True
        else:
            print("✗ Odstranění bylo zrušeno.")
            return False

    except Exception as e:
        session.rollback()
        print(f"✗ Chyba při odstraňování úkolu: {e}")
        return False
