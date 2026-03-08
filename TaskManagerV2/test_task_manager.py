import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Ukol, vytvorit_connection_string
from config import DATABASE_TYPE, TEST_DB_CONFIG

@pytest.fixture(scope='function')
def test_session():
    connection_string = vytvorit_connection_string(DATABASE_TYPE, TEST_DB_CONFIG[DATABASE_TYPE])
    engine = create_engine(connection_string, echo=False)

    # Vytvoření tabulek
    Base.metadata.create_all(engine)

    # Vytvoření session
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Cleanup - vyčištění testovacích dat
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


class TestPridatUkol:

    def test_pridat_ukol_pozitivni(self, test_session):
        novy_ukol = Ukol(
            nazev="Testovací úkol",
            popis="Popis testovacího úkolu",
            stav="Nezahájeno"
        )
        test_session.add(novy_ukol)
        test_session.commit()

        # Ověření
        ukol_z_db = test_session.query(Ukol).filter_by(nazev="Testovací úkol").first()

        assert ukol_z_db is not None, "Úkol nebyl nalezen v databázi"
        assert ukol_z_db.nazev == "Testovací úkol"
        assert ukol_z_db.popis == "Popis testovacího úkolu"
        assert ukol_z_db.stav == "Nezahájeno"
        assert ukol_z_db.id is not None, "ID úkolu nebylo přiřazeno"
        assert ukol_z_db.datum_vytvoreni is not None, "Datum vytvoření nebylo přiřazeno"

    def test_pridat_ukol_negativni_prazdny_nazev(self, test_session):
        # Pokus o přidání úkolu s prázdným názvem
        with pytest.raises(Exception):
            novy_ukol = Ukol(
                nazev=None,  # Název je povinný
                popis="Platný popis"
            )
            test_session.add(novy_ukol)
            test_session.commit()

        test_session.rollback()

        # Ověření, že žádný úkol nebyl přidán
        pocet_ukolu = test_session.query(Ukol).count()
        assert pocet_ukolu == 0, "Úkol s prázdným názvem by neměl být přidán"

    def test_pridat_ukol_negativni_prazdny_popis(self, test_session):
        with pytest.raises(Exception):
            novy_ukol = Ukol(
                nazev="Platný název",
                popis=None  # Popis je povinný
            )
            test_session.add(novy_ukol)
            test_session.commit()

        test_session.rollback()

        # Ověření
        pocet_ukolu = test_session.query(Ukol).count()
        assert pocet_ukolu == 0, "Úkol s prázdným popisem by neměl být přidán"


class TestAktualizovatUkol:

    def test_aktualizovat_ukol_pozitivni(self, test_session):
        # Přidání testovacího úkolu
        ukol = Ukol(
            nazev="Úkol k aktualizaci",
            popis="Tento úkol bude aktualizován",
            stav="Nezahájeno"
        )
        test_session.add(ukol)
        test_session.commit()
        ukol_id = ukol.id

        # Aktualizace stavu
        ukol_k_aktualizaci = test_session.query(Ukol).filter_by(id=ukol_id).first()
        ukol_k_aktualizaci.stav = "Probíhá"
        test_session.commit()

        # Ověření
        aktualizovany_ukol = test_session.query(Ukol).filter_by(id=ukol_id).first()
        assert aktualizovany_ukol.stav == "Probíhá", "Stav úkolu nebyl změněn"

    def test_aktualizovat_ukol_negativni_neexistujici_id(self, test_session):
        # Pokus o načtení neexistujícího úkolu
        neexistujici_ukol = test_session.query(Ukol).filter_by(id=9999).first()

        # Ověření
        assert neexistujici_ukol is None, "Neexistující úkol by měl vrátit None"

    def test_aktualizovat_ukol_pozitivni_na_hotovo(self, test_session):
        # Přidání úkolu
        ukol = Ukol(
            nazev="Úkol k dokončení",
            popis="Tento úkol bude označen jako hotový",
            stav="Probíhá"
        )
        test_session.add(ukol)
        test_session.commit()
        ukol_id = ukol.id

        # Aktualizace na Hotovo
        ukol.stav = "Hotovo"
        test_session.commit()

        # Ověření
        dokonceny_ukol = test_session.query(Ukol).filter_by(id=ukol_id).first()
        assert dokonceny_ukol.stav == "Hotovo"


class TestOdstranitUkol:

    def test_odstranit_ukol_pozitivni(self, test_session):
        # Přidání úkolu
        ukol = Ukol(
            nazev="Úkol k odstranění",
            popis="Tento úkol bude odstraněn",
            stav="Nezahájeno"
        )
        test_session.add(ukol)
        test_session.commit()
        ukol_id = ukol.id

        # Ověření, že úkol existuje
        assert test_session.query(Ukol).filter_by(id=ukol_id).first() is not None

        # Odstranění úkolu
        test_session.delete(ukol)
        test_session.commit()

        # Ověření, že úkol byl odstraněn
        odstraneny_ukol = test_session.query(Ukol).filter_by(id=ukol_id).first()
        assert odstraneny_ukol is None, "Úkol by měl být odstraněn z databáze"

    def test_odstranit_ukol_negativni_neexistujici_id(self, test_session):
        # Počet úkolů před pokusem o odstranění
        pocet_pred = test_session.query(Ukol).count()

        # Pokus o načtení neexistujícího úkolu
        neexistujici_ukol = test_session.query(Ukol).filter_by(id=9999).first()

        # Ověření
        assert neexistujici_ukol is None

        # Ověření, že počet úkolů se nezměnil
        pocet_po = test_session.query(Ukol).count()
        assert pocet_pred == pocet_po


class TestZobrazitUkoly:

    def test_zobrazit_ukoly_pozitivni_s_filtrem(self, test_session):
        # Přidání úkolů s různými stavy
        ukol1 = Ukol(nazev="Úkol 1", popis="Nezahájený", stav="Nezahájeno")
        ukol2 = Ukol(nazev="Úkol 2", popis="Probíhající", stav="Probíhá")
        ukol3 = Ukol(nazev="Úkol 3", popis="Dokončený", stav="Hotovo")

        test_session.add_all([ukol1, ukol2, ukol3])
        test_session.commit()

        # Načtení pouze aktivních úkolů
        aktivni_ukoly = test_session.query(Ukol).filter(
            Ukol.stav.in_(['Nezahájeno', 'Probíhá'])
        ).all()

        # Ověření
        assert len(aktivni_ukoly) == 2, "Měly by být vráceny 2 aktivní úkoly"
        assert all(u.stav in ['Nezahájeno', 'Probíhá'] for u in aktivni_ukoly)

    def test_zobrazit_ukoly_negativni_prazdny_seznam(self, test_session):
        # Načtení úkolů z prázdné databáze
        ukoly = test_session.query(Ukol).all()

        # Ověření
        assert len(ukoly) == 0, "Seznam úkolů by měl být prázdný"
        assert ukoly == [], "Měl by být vrácen prázdný seznam"


class TestKomplexniScenare:

    def test_kompletni_crud_cyklus(self, test_session):
        # 1. CREATE
        ukol = Ukol(
            nazev="CRUD test úkol",
            popis="Testování kompletního CRUD cyklu",
            stav="Nezahájeno"
        )
        test_session.add(ukol)
        test_session.commit()
        ukol_id = ukol.id

        # 2. READ
        naceny_ukol = test_session.query(Ukol).filter_by(id=ukol_id).first()
        assert naceny_ukol is not None
        assert naceny_ukol.nazev == "CRUD test úkol"

        # 3. UPDATE
        naceny_ukol.stav = "Probíhá"
        test_session.commit()

        # 4. Ověření UPDATE
        aktualizovany = test_session.query(Ukol).filter_by(id=ukol_id).first()
        assert aktualizovany.stav == "Probíhá"

        # 5. DELETE
        test_session.delete(aktualizovany)
        test_session.commit()

        # 6. Ověření DELETE
        odstraneny = test_session.query(Ukol).filter_by(id=ukol_id).first()
        assert odstraneny is None
