import datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dbSets import Task, Base
from vModels import VmTask
from taskStateEnum import StavUkolu

DB_NAME = "taskManager_db"
#uzivatelske jmeno, pri instalaci mysql se vytvori uzivatel root, ktery ma prava na vytvareni databazi
DB_USER = "root"
DB_PORT = "3306"
#heslo pro uzivatele postgres, pokud jsi si ho pri instalaci nastavil jine, zmen to tady, bei ti to na localhostu, takze to je fuk, jen to musi sedet s tim co jsi nastavil pri instalaci
# !!!! tohle je presne ten case, proc tohle ma jit uplne mimo code base, ptz ja pwd nemam a ty ano... takze porad si to musime menit, kdyby to slo outside ode me, tak jde muj setup a naopak tvuj setup, nebylo by to hardcoded
DB_PASS = ""
#hostitel, na kterem bezi postgresql server, pokud bezi na stejnem stroji jako tato aplikace, tak to muze zustat localhost
DB_HOST = "localhost"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class TaskManagerService:
    def __init__(self):
        self.db = None
        engine = create_engine(DATABASE_URL)
        if not database_exists(engine.url):
            print(f"Creating database {DB_NAME}")
            create_database(engine.url)
        self.engine = engine
        self.connection = self.engine.connect()
        self._initialize_tables()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = Base

    # helper co dela to odsazeni pomoci podtrzitek a vypisovani validovaneho vstupu od uzivatele
    @staticmethod
    def print_message_with_divider(message):
        print(f"\n{message}")
        print("_" * (len(message) + 1))

    # metoda pro ziskani validovaneho vstupu od uzivatele, ktery nesmi byt prazdny retezec, taky jsme uz probirali
    @staticmethod
    def get_validated_user_input(input_name, input_request_description, original_value: str = None):
        user_input = input(input_request_description)
        while original_value is None and user_input == "":
            print(f"\033[93m{input_name} cannot be empty. Please try again.\033[0m")
            user_input = input(input_request_description)

        if original_value is not None and user_input == "":
            return original_value

        return user_input

    # tohle je metoda pro mapovani entity Task z databaze na view model VmTask, ktery se pak pouziva pro prelozeni db modelu na model pouzivany v aplikaci
    @staticmethod
    def task_entity_to_view_model(task_entity: Task) -> VmTask:
        return VmTask(
            task_id = task_entity.id,
            nazev = task_entity.Nazev,
            popis = task_entity.Popis,
            smazan = task_entity.JeSmazan,
            stav = StavUkolu(task_entity.Stav),
            vytvoren = task_entity.Vytvoren,
            updated_at = task_entity.Aktualizovan
        )

    # to same jako vyse ale pro seznam entit
    def map_task_entities_to_view_models(self, entities: list[Task]) -> list[VmTask]:
        return [
            self.task_entity_to_view_model(entity)
            for entity in entities
        ]

    def handle_user_input(self, user_choice: int):
        #jelikoz uz je sice check v tride menu a nemela by ti tady prijit jina nez 1-5, tak pro jistotu to tady checknu znovu, jestli
        #mi neprislo nejake hovno, porad musis pocitat s tim, ze tuhle servisu si muze vytvorit kdokoliv bez toho, aby pouzival menu,
        #takze si porad musis kontrolovat vstup do teto metody a jestli je opravdu validni

        self.db = self.SessionLocal()

        try:
            match user_choice:
                case 1:
                    self.__handle_add_task()
                case 2:
                    self.__update_task()
                case 3:
                    self.__list_tasks([StavUkolu.Nezahajeno.value, StavUkolu.Probiha.value])
                case 4:
                    self.__list_tasks([StavUkolu.Nezahajeno.value, StavUkolu.Probiha.value], True)
                case 5:
                    self.__delete_task()
                case _:
                    print("The value you have provided does not correspond to any available option.")

        except Exception as e:
            #kdyz nastane chyba, tak provedu rollback, aby se zmeny neprojevily v databazi
            self.db.rollback()
            print(f"Error adding task: {e}")
        finally:
            #uzavru spojeni s databazi
            self.db.close()

        print("\n")

    def __handle_add_task(self):
        print("\nPlease provide the following details to create a new task.")
        #to jsme uz resili, mam udelany helper pro ziskani validniho vstupu od uzivatele
        task_name = self.get_validated_user_input("Task name", "\nEnter task name: ")
        task_description = self.get_validated_user_input("Task description", "\nEnter task description: ")
        task = self.__add_task(task_name, task_description)
        print(f"\033[92m\nTask {task.Nazev} added with ID: {task.task_id}\033[0m")

    def __add_task(self, nazev: str, popis: str) -> VmTask | None:
        result = None
        #vytvorim si novou databazovou entitu
        new_task = Task(Nazev = nazev, Popis = popis, Stav = StavUkolu.Nezahajeno.value)

        #pridam ji do session (transakce/databaze)
        self.db.add(new_task)

        #commitnu zmeny do databaze, cimz se nova entita skutecne ulozi na databazovem serveru
        self.db.commit()

        #pred ukoncenim spojeni s databazi si musim refreshnout entitu, aby se mi nahrala hodnota id, ktera se generuje automaticky pri vlozeni do db
        self.db.refresh(new_task)
        #prevedu databazovou entitu na view model, ktery se pak zobrazuje do uzivatelskeho rozhrani
        return self.task_entity_to_view_model(new_task)

    def __update_task(self):
        user_input = None
        self.__list_tasks([StavUkolu.Nezahajeno.value, StavUkolu.Probiha.value])
        self.print_message_with_divider("Update Task:")
        while True:
            task_id_input = self.get_validated_user_input("Task ID", "Enter task ID to update: ")
            
            try:
                task_id = int(task_id_input)
                # zkusim najit task podle id
                task = self.db.query(Task).filter(Task.id == task_id, Task.JeSmazan == False).first()
                if task:
                    print(f"1. Probiha, 2. Hotovo, 0 pro ukonceni bez zmeny")
                    state_input = input("Zvol moznost: ")
                    while state_input == "" or state_input not in ["0","1","2"]:
                        print(f"\033[93mInvalid option. Please try again.\033[0m")
                        state_input = input("Zvol moznost: ")

                    if state_input == "0":
                        print("\033[93mUpdate operation cancelled by user.\033[0m")
                        break

                    task.Stav = int(state_input) + 1
                    task.Aktualizovan = datetime.datetime.now(datetime.UTC)
                    self.db.commit()
                    self.db.refresh(task)
                    updated_task = self.task_entity_to_view_model(task)
                    print(f"\033[92m\nTask {updated_task.Nazev} with ID: {updated_task.task_id} has been updated\033[0m")
                    break
                else:
                    print("\033[93mTask ID does not exist or is deleted. Please enter existing TaskID.\033[0m")
            except ValueError:
                print("\033[93mInvalid Task ID. Please enter a numeric value.\033[0m")

    def __list_tasks(self, status_list = None, include_deleted = False):
        if status_list is None:
            status_list = []
        self.print_message_with_divider("Listing all tasks:")
        #ziskam vsechny tasky, podle toho jestli chci i smazane nebo ne na zaklade parametru include_deleted
        if include_deleted:
            all_available_tasks = self.db.query(Task).all()
        else:
            all_available_tasks = self.db.query(Task).filter(Task.JeSmazan == False, Task.Stav.in_(status_list)).all()

        sed = self.db.query(Task).all()

        for task in all_available_tasks:
            print(f"ID: {task.id}, Nazev: {task.Nazev}, Popis: {task.Popis}, Stav: {StavUkolu(task.Stav).name}, Vytvoren: {task.Vytvoren}, Aktualizovan: {task.Aktualizovan}")
        if len(all_available_tasks) == 0:
            print("\033[93mNo tasks available.\033[0m")

    def __delete_task(self) -> VmTask | None:
        is_deleted = False
        result = None

        while not is_deleted:
            task_id_input = self.get_validated_user_input("Task ID", "Enter task ID to delete (or 0 to exit delete operation): ")
            try:
                task_id = int(task_id_input)
                if task_id == 0:
                    print("\033[93mDelete operation cancelled by user.\033[0m")
                    break
                # zkusim najit task podle id
                task = self.db.query(Task).filter(Task.id == task_id, Task.JeSmazan == False).first()
                if task:
                    # kdyz jsem nasel, oznacim ho jako smazany
                    task.JeSmazan = True
                    task.Aktualizovan = datetime.datetime.now(datetime.UTC)
                    task.Stav = StavUkolu.Hotovo.value
                    is_deleted = True
                    self.db.commit()
                    result = self.task_entity_to_view_model(task)
                    print(f"\033[92m\nTask {task.Nazev} with ID: {task.id} has been removed\033[0m")
                else:
                    print("\033[93mTask ID does not exist. Please enter existing TaskID.\033[0m")
            except ValueError:
                print("\033[93mInvalid Task ID. Please enter a numeric value.\033[0m")

        return result

    def _initialize_tables(self):
        # tohle jsem udelal na prasaka, ale pro jednoduchost to takhle necham, aby se tabulky vytvorily pokud jeste neexistuji
        print("Attempting to create tables...")
        Base.metadata.create_all(self.engine)
        print("Tables created (if they didn't exist).")