from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_TYPE, DB_CONFIG

Base = declarative_base()


class Ukol(Base):
    __tablename__ = 'ukoly'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nazev = Column(String(200), nullable=False)
    popis = Column(String(500), nullable=False)
    stav = Column(String(50), default='Nezahájeno')
    datum_vytvoreni = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Ukol(id={self.id}, nazev='{self.nazev}', stav='{self.stav}')>"


def vytvorit_connection_string(db_type=None, config=None):
    if db_type is None:
        db_type = DATABASE_TYPE

    if config is None:
        config = DB_CONFIG[db_type]

    if db_type == 'mysql':
        return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    else:
        raise ValueError(f"Nepodporovaný typ databáze: {db_type}")


def pripojeni_db(db_type=None, config=None):
    try:
        connection_string = vytvorit_connection_string(db_type, config)
        engine = create_engine(connection_string, echo=False)
        with engine.connect() as connection:
            print(f"✓ Připojení k databázi bylo úspěšné! (Typ: {db_type or DATABASE_TYPE})")

        Session = sessionmaker(bind=engine)
        return engine, Session

    except Exception as e:
        print(f"✗ Chyba při připojení k databázi: {e}")
        return None, None


def vytvoreni_tabulky(engine):
    try:
        Base.metadata.create_all(engine)
        print("✓ Tabulka 'ukoly' je připravena k použití.")
        return True
    except Exception as e:
        print(f"✗ Chyba při vytváření tabulky: {e}")
        return False