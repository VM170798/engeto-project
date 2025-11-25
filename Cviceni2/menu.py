from Cviceni2.taskManagerService import TaskManagerService

class Menu:
    task_manager_service = None
    def __init__(self):
        # vytvarim si manazera uloh pokud jeste neni vytvoren
        if self.task_manager_service is None:
            self.task_manager_service = TaskManagerService()

    @staticmethod
    #metoda pro ziskani volby uzivatele s validaci
    #staticka metoda protoze nepotrebuje pristup k instancnim promennym teto tridy
    def get_choice():
        while True:
            try:
                choice = int(input("\nZadejte cislo volby: "))
                if choice in [1, 2, 3, 4, 5, 6]:
                    return choice
                else:
                    print("\033[93mVolba je neplatna. Zkuste to prosim znovu.\033[0m")
            except ValueError:
                print("\033[93mNeplatny vstup. Prosim vlozte cislo z horni nabidky.\033[0m")

    #metoda pro zobrazeni menu a zpracovani volby uzivatele
    def show(self):
        print("\nVitejte ve vylepsenem Task Manager s MySql DB!")

        while True:
            print("Prosim zvolte volbu:")
            print("1. Vytvorit Zadani")
            print("2. Aktualizovat Zadani")
            print("3. Zobraz vsechna zadani")
            print("4. Zobraz vsechna zadani (vcetne vymazanych)")
            print("5. Odstranit zadani")
            print("6. Ukoncil program")
            user_choice = self.get_choice()

            #ukoncujem program, pokud uzivatel zvoli 6, ale da se to resit i jinak
            if user_choice == 6:
                print("\nDekuji ze pouzivate Task Manager. Nashledanou!")
                exit()
            else:
                #tady to pro zjednoduseni necham zpracovat tou servisou, ktera si sama kontroluje vstup a jestli vstup je validni
                self.task_manager_service.handle_user_input(user_choice)