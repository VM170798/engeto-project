from taskManagerService import TaskManagerService

class Menu:
    task_manager_service = None
    def __init__(self):
       
        if self.task_manager_service is None:
            self.task_manager_service = TaskManagerService()

    @staticmethod
    
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

           
            if user_choice == 6:
                print("\nDekuji ze pouzivate Task Manager. Nashledanou!")
                exit()
            else:
                
                self.task_manager_service.handle_user_input(user_choice)