import datetime

from taskStateEnum import StavUkolu

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
        return f"ID: {self.task_id}, Jmeno: {self.Nazev}, Popis: {self.Popis}, Stav: {self.Stav.name}, Je smazan: {self.JeSmazan}, Vytvoren: {self.vytvoren}, Aktualizovan: {self.aktualizovan}"