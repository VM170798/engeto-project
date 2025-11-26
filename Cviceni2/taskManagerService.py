import datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dbSets import Task, Base
from vModels import VmTask
from taskStateEnum import StavUkolu

DB_NAME = "taskManager_db"

DB_USER = "root"
DB_PORT = "3306"

DB_PASS = "Czclone1998"

DB_HOST = "localhost"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class TaskManagerService:
    def __init__(self):
        self.db = None
        try:
            engine = create_engine(DATABASE_URL)
            if not database_exists(engine.url):
                print(f"Vytvor databazi {DB_NAME}")
                create_database(engine.url)
            self.engine = engine

            self.connection = self.engine.connect()
        except Exception as e:
            print("neni DB")
            exit()
        self._initialize_tables()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = Base

   
    @staticmethod
    def print_message_with_divider(message):
        print(f"\n{message}")
        print("_" * (len(message) + 1))

    
    @staticmethod
    def get_validated_user_input(input_name, input_request_description, original_value: str = None):
        user_input = input(input_request_description)
        while original_value is None and user_input == "":
            print(f"\033[93m{input_name} nesmi byt prazdny. Zkuste prosim znovu.\033[0m")
            user_input = input(input_request_description)

        if original_value is not None and user_input == "":
            return original_value

        return user_input

   
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

    
    def map_task_entities_to_view_models(self, entities: list[Task]) -> list[VmTask]:
        return [
            self.task_entity_to_view_model(entity)
            for entity in entities
        ]

    def handle_user_input(self, user_choice: int):
        

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
                    print("Zadaná hodnota neodpovídá žádné dostupné možnosti..")

        except Exception as e:
           
            self.db.rollback()
            print(f"Chyba zadani ukolu: {e}")
        finally:
            
            self.db.close()

        print("\n")

    def __handle_add_task(self):
        print("\n„Zadejte následující údaje pro vytvoření nového úkolu.")
       
        task_name = self.get_validated_user_input("Nazev ukolu", "\nZadejte jmeno ukolu: ")
        task_description = self.get_validated_user_input("Popis ukolu", "\nVlozte popis ukolu: ")
        task = self.__add_task(task_name, task_description)
        print(f"\033[92m\nUkol {task.Nazev} addeVlozte s ID: {task.task_id}\033[0m")

    def __add_task(self, nazev: str, popis: str) -> VmTask | None:
        result = None
      
        new_task = Task(Nazev = nazev, Popis = popis, Stav = StavUkolu.Nezahajeno.value)

        
        self.db.add(new_task)

       
        self.db.commit()

        
        self.db.refresh(new_task)
       
        return self.task_entity_to_view_model(new_task)

    def __update_task(self):
        user_input = None
        self.__list_tasks([StavUkolu.Nezahajeno.value, StavUkolu.Probiha.value])
        self.print_message_with_divider("Aktualizovat ukol:")
        while True:
            task_id_input = self.get_validated_user_input("ID ukolu", "Vlozte ID ukolu pro aktualizaci: ")
            
            try:
                task_id = int(task_id_input)
              
                task = self.db.query(Task).filter(Task.id == task_id, Task.JeSmazan == False).first()
                if task:
                    print(f"1. Probiha, 2. Hotovo, 0 pro ukonceni bez zmeny")
                    state_input = input("Zvol moznost: ")
                    while state_input == "" or state_input not in ["0","1","2"]:
                        print(f"\033[93mNeplatna moznost. Prosim zkuste znovu.\033[0m")
                        state_input = input("Zvol moznost: ")

                    if state_input == "0":
                        print("\033[93m„Aktualizace byla zrušena uživatelem.\033[0m")
                        break

                    task.Stav = int(state_input) + 1
                    task.Aktualizovan = datetime.datetime.now(datetime.UTC)
                    self.db.commit()
                    self.db.refresh(task)
                    updated_task = self.task_entity_to_view_model(task)
                    print(f"\033[92m\nUkol {updated_task.Nazev} s ID: {updated_task.task_id} byl aktualizovan\033[0m")
                    break
                else:
                    print("\033[93mID ukolu neexistuje nebo byl odstranen. Please enter platne ID ukolu.\033[0m")
            except ValueError:
                print("\033[93mneplatne ID ukolu. Prosim vlozte ciselnou hodnotu ID.\033[0m")

    def __list_tasks(self, status_list = None, include_deleted = False):
        if status_list is None:
            status_list = []
        self.print_message_with_divider("Seznam vsech ukolu:")
       
        if include_deleted:
            all_available_tasks = self.db.query(Task).all()
        else:
            all_available_tasks = self.db.query(Task).filter(Task.JeSmazan == False, Task.Stav.in_(status_list)).all()

        sed = self.db.query(Task).all()

        for task in all_available_tasks:
            print(f"ID: {task.id}, Nazev: {task.Nazev}, Popis: {task.Popis}, Stav: {StavUkolu(task.Stav).name}, Vytvoren: {task.Vytvoren}, Aktualizovan: {task.Aktualizovan}")
        if len(all_available_tasks) == 0:
            print("\033[93mZadne dostupne ukoly.\033[0m")

    def __delete_task(self) -> VmTask | None:
        is_deleted = False
        result = None

        while not is_deleted:
            task_id_input = self.get_validated_user_input("ID Ukolu", "Zadejte ID úkolu pro smazání (zadejte 0 pro ukončení operace mazání): ")
            try:
                task_id = int(task_id_input)
                if task_id == 0:
                    print("\033[93mMazání bylo zrušeno uživatelem.\033[0m")
                    break
              
                task = self.db.query(Task).filter(Task.id == task_id, Task.JeSmazan == False).first()
                if task:
                 
                    task.JeSmazan = True
                    task.Aktualizovan = datetime.datetime.now(datetime.UTC)
                    task.Stav = StavUkolu.Hotovo.value
                    is_deleted = True
                    self.db.commit()
                    result = self.task_entity_to_view_model(task)
                    print(f"\033[92m\nUkol {task.Nazev} s ID: {task.id} byl odebran\033[0m")
                else:
                    print("\033[93mID ukolu neexistuje. Prosim vlozte platne ID ukolu.\033[0m")
            except ValueError:
                print("\033[93mNeplatne ID ukolu. Prosim vlozte platne cislo.\033[0m")

        return result

    def _initialize_tables(self):
       
        print("Probíhá pokus o vytvoření tabulek...")
        Base.metadata.create_all(self.engine)
        print("Tabulka vytvořena (pokud neexistuje).")