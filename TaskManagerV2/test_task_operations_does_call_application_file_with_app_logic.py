import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Ukol, vytvorit_connection_string
from config import DATABASE_TYPE, TEST_DB_CONFIG
from task_operations import pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol
import sys
from io import StringIO

@pytest.fixture(scope='function')
def test_session():
    connection_string = vytvorit_connection_string(DATABASE_TYPE, TEST_DB_CONFIG[DATABASE_TYPE])
    engine = create_engine(connection_string, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()

# --- pridat_ukol ---
def test_pridat_ukol_pozitivni(monkeypatch, test_session):
    inputs = iter(["Testovací úkol", "Popis testovacího úkolu"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert pridat_ukol(test_session) is True
    ukol = test_session.query(Ukol).filter_by(nazev="Testovací úkol").first()
    assert ukol is not None
    assert ukol.popis == "Popis testovacího úkolu"
    assert ukol.stav == "Nezahájeno"

def test_pridat_ukol_negativni_prazdny_nazev(monkeypatch, test_session):
    inputs = iter(["", "Testovací úkol", "Popis testovacího úkolu"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert pridat_ukol(test_session) is True
    ukol = test_session.query(Ukol).filter_by(nazev="Testovací úkol").first()
    assert ukol is not None

def test_pridat_ukol_negativni_prazdny_popis(monkeypatch, test_session):
    inputs = iter(["Testovací úkol", "", "Popis testovacího úkolu"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert pridat_ukol(test_session) is True
    ukol = test_session.query(Ukol).filter_by(nazev="Testovací úkol").first()
    assert ukol is not None

# --- zobrazit_ukoly ---
def test_zobrazit_ukoly_pozitivni(test_session, capsys):
    test_session.add_all([
        Ukol(nazev="Ukol1", popis="Popis1", stav="Nezahájeno"),
        Ukol(nazev="Ukol2", popis="Popis2", stav="Probíhá"),
        Ukol(nazev="Ukol3", popis="Popis3", stav="Hotovo")
    ])
    test_session.commit()
    zobrazit_ukoly(test_session)
    captured = capsys.readouterr()
    assert "Ukol1" in captured.out
    assert "Ukol2" in captured.out
    assert "Ukol3" not in captured.out

def test_zobrazit_ukoly_negativni_prazdny(test_session, capsys):
    zobrazit_ukoly(test_session)
    captured = capsys.readouterr()
    assert "prázdný" in captured.out

# --- aktualizovat_ukol ---
def test_aktualizovat_ukol_pozitivni(monkeypatch, test_session):
    ukol = Ukol(nazev="Aktualizace", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter([str(ukol.id), "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert aktualizovat_ukol(test_session) is True
    test_session.refresh(ukol)
    assert ukol.stav == "Probíhá"

def test_aktualizovat_ukol_negativni_neexistujici_id(monkeypatch, test_session, capsys):
    ukol = Ukol(nazev="Aktualizace", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter(["9999", str(ukol.id), "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert aktualizovat_ukol(test_session) is True
    test_session.refresh(ukol)
    assert ukol.stav == "Hotovo"

# --- odstranit_ukol ---
def test_odstranit_ukol_pozitivni(monkeypatch, test_session):
    ukol = Ukol(nazev="Odstranit", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter([str(ukol.id), "ano"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert odstranit_ukol(test_session) is True
    assert test_session.query(Ukol).filter_by(id=ukol.id).first() is None

def test_odstranit_ukol_negativni_neexistujici_id(monkeypatch, test_session, capsys):
    ukol = Ukol(nazev="Odstranit", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter(["9999", str(ukol.id), "ano"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert odstranit_ukol(test_session) is True
    assert test_session.query(Ukol).filter_by(id=ukol.id).first() is None

def test_odstranit_ukol_negativni_zruseno(monkeypatch, test_session):
    ukol = Ukol(nazev="Odstranit", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter([str(ukol.id), "ne"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert odstranit_ukol(test_session) is False
    assert test_session.query(Ukol).filter_by(id=ukol.id).first() is not None

# --- pridat_ukol: exception branch (lines 31-34) ---
def test_pridat_ukol_exception_vraci_false(monkeypatch, test_session):
    inputs = iter(["Nazev", "Popis"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch.object(test_session, 'commit', side_effect=Exception("DB chyba")):
        result = pridat_ukol(test_session)
    assert result is False

# --- zobrazit_ukoly: exception branch (lines 57-58) ---
def test_zobrazit_ukoly_exception(monkeypatch, test_session, capsys):
    with patch.object(test_session, 'query', side_effect=Exception("DB chyba")):
        zobrazit_ukoly(test_session)
    captured = capsys.readouterr()
    assert "Chyba" in captured.out

# --- aktualizovat_ukol: empty list → return False (lines 69-70) ---
def test_aktualizovat_ukol_negativni_prazdny_seznam(test_session, capsys):
    result = aktualizovat_ukol(test_session)
    assert result is False
    captured = capsys.readouterr()
    assert "aktualizaci" in captured.out

# --- aktualizovat_ukol: non-numeric ID input → ValueError (lines 86-87) ---
def test_aktualizovat_ukol_neplatne_id_neni_cislo(monkeypatch, test_session):
    ukol = Ukol(nazev="Aktualizace", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter(["abc", str(ukol.id), "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert aktualizovat_ukol(test_session) is True
    test_session.refresh(ukol)
    assert ukol.stav == "Probíhá"

# --- aktualizovat_ukol: invalid state choice → retry (line 101) ---
def test_aktualizovat_ukol_neplatna_volba_stavu(monkeypatch, test_session):
    ukol = Ukol(nazev="Aktualizace", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter([str(ukol.id), "9", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert aktualizovat_ukol(test_session) is True
    test_session.refresh(ukol)
    assert ukol.stav == "Hotovo"

# --- aktualizovat_ukol: exception branch (lines 108-111) ---
def test_aktualizovat_ukol_exception_vraci_false(monkeypatch, test_session):
    ukol = Ukol(nazev="Aktualizace", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter([str(ukol.id), "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch.object(test_session, 'commit', side_effect=Exception("DB chyba")):
        result = aktualizovat_ukol(test_session)
    assert result is False

# --- odstranit_ukol: empty list → return False (lines 120-121) ---
def test_odstranit_ukol_negativni_prazdny_seznam(test_session, capsys):
    result = odstranit_ukol(test_session)
    assert result is False
    captured = capsys.readouterr()
    assert "odstranění" in captured.out

# --- odstranit_ukol: non-numeric ID input → ValueError (lines 137-138) ---
def test_odstranit_ukol_neplatne_id_neni_cislo(monkeypatch, test_session):
    ukol = Ukol(nazev="Odstranit", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter(["abc", str(ukol.id), "ano"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert odstranit_ukol(test_session) is True
    assert test_session.query(Ukol).filter_by(id=ukol.id).first() is None

# --- odstranit_ukol: exception branch (lines 150-153) ---
def test_odstranit_ukol_exception_vraci_false(monkeypatch, test_session):
    ukol = Ukol(nazev="Odstranit", popis="Popis", stav="Nezahájeno")
    test_session.add(ukol)
    test_session.commit()
    inputs = iter([str(ukol.id), "ano"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch.object(test_session, 'commit', side_effect=Exception("DB chyba")):
        result = odstranit_ukol(test_session)
    assert result is False