import datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dbSets import Task, Base
from vModels import VmTask
from taskStateEnum import TaskStatus

DB_NAME = "taskManager_db"
#uzivatelske jmeno, pri instalaci mysql se vytvori uzivatel root, ktery ma prava na vytvareni databazi
DB_USER = "root"
DB_PORT = "3306"
#heslo pro uzivatele postgres, pokud jsi si ho pri instalaci nastavil jine, zmen to tady, bei ti to na localhostu, takze to je fuk, jen to musi sedet s tim co jsi nastavil pri instalaci
DB_PASS = "Czclone1998"
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
            task_id=task_entity.id,
            name=task_entity.name,
            description=task_entity.description,
            is_deleted=task_entity.is_deleted,
            status=TaskStatus(task_entity.status),
            created_at=task_entity.created_at,
            updated_at=task_entity.updated_at
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
                    self.__list_tasks([TaskStatus.Nezahajeno.value, TaskStatus.Probiha.value])
                case 4:
                    self.__list_tasks([TaskStatus.Nezahajeno.value, TaskStatus.Probiha.value], True)
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
        print(f"\033[92m\nTask {task.name} added with ID: {task.task_id}\033[0m")

    def __add_task(self, name: str, description: str) -> VmTask | None:
        result = None
        #vytvorim si novou databazovou entitu
        new_task = Task(name=name, description=description, status=TaskStatus.Nezahajeno.value)

        #pridam ji do session (transakce/databaze)
        self.db.add(new_task)

        #commitnu zmeny do databaze, cimz se nova entita skutecne ulozi na databazovem serveru
        self.db.commit()

        #pred ukoncenim spojeni s databazi si musim refreshnout entitu, aby se mi nahrala hodnota id, ktera se generuje automaticky pri vlozeni do db
        self.db.refresh(new_task)
        #prevedu databazovou entitu na view model, ktery se pak zobrazuje do uzivatelskeho rozhrani
        return self.task_entity_to_view_model(new_task)

    def __update_task(self):
        self.__list_tasks([TaskStatus.Nezahajeno.value, TaskStatus.Probiha.value])
        self.print_message_with_divider("Update Task:")
        while True:
            task_id_input = self.get_validated_user_input("Task ID", "Enter task ID to update: ")
            
            try:
                task_id = int(task_id_input)
                # zkusim najit task podle id
                task = self.db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
                if task:
                    while user_input == "" or user_input not in [1,2]:
                        print(f"\033[93m1. Hotovo, 2. Probiha\033[0m")
                        user_input = input("Zvol moznost")
                    
                    task.Stav = int(user_input) + 1
                    task.updated_at = datetime.datetime.now(datetime.UTC)
                    self.db.commit()
                    self.db.refresh(task)
                    updated_task = self.task_entity_to_view_model(task)
                    print(f"\033[92m\nTask {updated_task.name} with ID: {updated_task.task_id} has been updated\033[0m")
                    break
                else:
                    print("\033[93mTask ID does not exist or is deleted. Please enter existing TaskID.\033[0m")
            except ValueError:
                print("\033[93mInvalid Task ID. Please enter a numeric value.\033[0m")

    def __list_tasks(self, status_list: List[int] = [], include_deleted = False):
        self.print_message_with_divider("Listing all tasks:")
        #ziskam vsechny tasky, podle toho jestli chci i smazane nebo ne na zaklade parametru include_deleted
        if include_deleted:
            all_available_tasks = self.db.query(Task).all()
        else:
            all_available_tasks = self.db.query(Task).filter(Task.is_deleted == False, Task.Stav in [status_list]).all()

        for task in all_available_tasks:
            print(f"ID: {task.id}, Name: {task.name}, Description: {task.description}, Status: {TaskStatus(task.status).name}, Created At: {task.created_at}, Updated At: {task.updated_at}")
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
                task = self.db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
                if task:
                    # kdyz jsem nasel, oznacim ho jako smazany
                    task.is_deleted = True
                    task.updated_at = datetime.datetime.now(datetime.UTC)
                    task.status = TaskStatus.Closed.value
                    is_deleted = True
                    self.db.commit()
                    result = self.task_entity_to_view_model(task)
                    print(f"\033[92m\nTask {task.name} with ID: {task.id} has been removed\033[0m")
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