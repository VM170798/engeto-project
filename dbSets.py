from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

# Definice databázového modelu pro tasky, tak jak se ti vytvori tabulka v databazi (z dokumentace SQLAlchemy)
class Task(Base):
    __tablename__ = 'UKOLY'

    # Definice sloupcu tabulky
    id = Column(Integer, primary_key=True, autoincrement=True)
    Jmeno = Column(String(50), nullable=False)
    Popis = Column(String(250), nullable=False)
    smazano = Column(Boolean, default=False)
    Stav = Column(Integer, nullable=False)
    Vytvoreno = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    # Ukazka toho jak si muzes definovat reprezentaci teto tridy pro lepsi vypis do konzole nebo logu pri pouziti funkce print() nebo str()
    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}, Description: {self.description}, Is Deleted: {self.is_deleted}, Status: {self.status}, Created At: {self.created_at}, Updated At: {self.updated_at}"