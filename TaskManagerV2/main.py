from database import pripojeni_db, vytvoreni_tabulky
from task_operations import pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol

def hlavni_menu():
    while True:
        print("\n" + "=" * 50)
        print("        TASK MANAGER - Správce úkolů")
        print("=" * 50)
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        print("=" * 50)

        volba = input("Vyberte možnost (1-5): ").strip()

        if volba == '1':
            pridat_ukol(session)
        elif volba == '2':
            zobrazit_ukoly(session)
        elif volba == '3':
            aktualizovat_ukol(session)
        elif volba == '4':
            odstranit_ukol(session)
        elif volba == '5':
            print("\n👋 Ukončuji program. Na shledanou!")
            break
        else:
            print("⚠ Neplatná volba! Zadejte prosím číslo 1-5.")

if __name__ == '__main__':
    print("🚀 Spouštím Task Manager...")
    engine, Session = pripojeni_db()
    if engine is None or Session is None:
        print("✗ Nepodařilo se připojit k databázi. Program se ukončuje.")
        exit(1)
    vytvoreni_tabulky(engine)
    session = Session()
    try:
        hlavni_menu()
    finally:
        session.close()
        print("✓ Připojení k databázi bylo uzavřeno.")
