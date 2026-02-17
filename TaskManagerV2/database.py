"""
Database connection and operations module.
This module handles all database operations using SQLAlchemy ORM.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_TYPE, DB_CONFIG

# Base class for all models
Base = declarative_base()


class Ukol(Base):
    """Model pro tabulku ukoly (Task model)"""
    __tablename__ = 'ukoly'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nazev = Column(String(200), nullable=False)
    popis = Column(String(500), nullable=False)
    stav = Column(String(50), default='Nezahájeno')
    datum_vytvoreni = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Ukol(id={self.id}, nazev='{self.nazev}', stav='{self.stav}')>"


def vytvorit_connection_string(db_type=None, config=None):
    """
    Vytvoří connection string pro připojení k databázi.

    Args:
        db_type: Typ databáze ('mysql', 'postgresql', 'mssql', 'sqlite')
        config: Konfigurační slovník s parametry připojení

    Returns:
        str: Connection string pro SQLAlchemy
    """
    if db_type is None:
        db_type = DATABASE_TYPE

    if config is None:
        config = DB_CONFIG[db_type]

    if db_type == 'mysql':
        return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    elif db_type == 'postgresql':
        return f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    elif db_type == 'mssql':
        return f"mssql+pyodbc://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?driver=ODBC+Driver+17+for+SQL+Server"
    elif db_type == 'sqlite':
        return f"sqlite:///{config['database']}"
    else:
        raise ValueError(f"Nepodporovaný typ databáze: {db_type}")


def pripojeni_db(db_type=None, config=None):
    """
    Připojení k databázi.

    Args:
        db_type: Typ databáze (pokud None, použije se z configu)
        config: Konfigurační slovník (pokud None, použije se z configu)

    Returns:
        tuple: (engine, Session) - engine pro správu připojení a Session pro transakce
    """
    try:
        connection_string = vytvorit_connection_string(db_type, config)
        engine = create_engine(connection_string, echo=False)

        # Otestujeme připojení
        with engine.connect() as connection:
            print(f"✓ Připojení k databázi bylo úspěšné! (Typ: {db_type or DATABASE_TYPE})")

        Session = sessionmaker(bind=engine)
        return engine, Session

    except Exception as e:
        print(f"✗ Chyba při připojení k databázi: {e}")
        return None, None


def vytvoreni_tabulky(engine):
    """
    Vytvoření tabulky ukoly, pokud neexistuje.

    Args:
        engine: SQLAlchemy engine objekt
    """
    try:
        Base.metadata.create_all(engine)
        print("✓ Tabulka 'ukoly' je připravena k použití.")
        return True
    except Exception as e:
        print(f"✗ Chyba při vytváření tabulky: {e}")
        return False
