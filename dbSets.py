from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

# Definice databázového modelu pro tasky, tak jak se ti vytvori tabulka v databazi (z dokumentace SQLAlchemy)
class Task(Base):
    __tablename__ = 'ukoly'

    # Definice sloupcu tabulky
    id = Column(Integer, primary_key=True, autoincrement=True)
    Nazev = Column(String(50), nullable=False)
    Popis = Column(String(250), nullable=False)
    JeSmazan = Column(Boolean, default=False)
    Stav = Column(Integer, nullable=False)
    Vytvoren = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    Aktualizovan = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    # Ukazka toho jak si muzes definovat reprezentaci teto tridy pro lepsi vypis do konzole nebo logu pri pouziti funkce print() nebo str()
    def __repr__(self):
        return f"ID: {self.id}, Nazev: {self.Nazev}, Popis: {self.Popis}, Je oznacen jako smazany: {self.JeSmazan}, Stav: {self.Stav}, Vytvoren: {self.Vytvoren}, Aktualizovan {self.Aktualizovan}"