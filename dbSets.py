from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

# Definice databázového modelu pro tasky, tak jak se ti vytvori tabulka v databazi (z dokumentace SQLAlchemy)
class Task(Base):
    __tablename__ = 'tasks'

    # Definice sloupcu tabulky
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)
    is_deleted = Column(Boolean, default=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    # Ukazka toho jak si muzes definovat reprezentaci teto tridy pro lepsi vypis do konzole nebo logu pri pouziti funkce print() nebo str()
    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}, Description: {self.description}, Is Deleted: {self.is_deleted}, Status: {self.status}, Created At: {self.created_at}, Updated At: {self.updated_at}"