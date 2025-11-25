import datetime

from Cviceni2.taskStateEnum import StavUkolu

class VmTask:
    def __init__(self, task_id, nazev: str, popis: str, stav: StavUkolu, vytvoren: datetime.datetime, updated_at: datetime.datetime, smazan=False):
        self.task_id = task_id
        self.Nazev = nazev
        self.Popis = popis
        self.Stav = stav
        self.JeSmazan = smazan
        self.vytvoren = vytvoren
        self.aktualizovan = updated_at

    def __repr__(self):
        return f"ID: {self.task_id}, Name: {self.Nazev}, Description: {self.Popis}, Status: {self.Stav.name}, Is Deleted: {self.JeSmazan}, Created At: {self.vytvoren}, Updated At: {self.aktualizovan}"