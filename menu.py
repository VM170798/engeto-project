from taskManagerService import TaskManagerService


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
                choice = int(input("\nEnter your choice: "))
                if choice in [1, 2, 3, 4, 5, 6]:
                    return choice
                else:
                    print("\033[93mOption does not exist. Please try again.\033[0m")
            except ValueError:
                print("\033[93mInvalid input. Please enter a number from the options above.\033[0m")

    #metoda pro zobrazeni menu a zpracovani volby uzivatele
    def show(self):
        print("\nWelcome to the enhanced Task Manager with MySql DB!")

        while True:
            print("Please choose an option:")
            print("1. Create Task")
            print("2. Update Task")
            print("3. List all tasks")
            print("4. List all tasks (deleted included)")
            print("5. Remove task")
            print("6. Exit program")
            user_choice = self.get_choice()

            #ukoncujem program, pokud uzivatel zvoli 6, ale da se to resit i jinak
            if user_choice == 6:
                print("\nThank you for using the Task Manager. Goodbye!")
                exit()
            else:
                #tady to pro zjednoduseni necham zpracovat tou servisou, ktera si sama kontroluje vstup a jestli vstup je validni
                self.task_manager_service.handle_user_input(user_choice)