import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Ukol
from task_operations import pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol
from config import TEST_DB_CONFIG
from unittest.mock import patch
import io


@pytest.fixture
def test_db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestPridatUkol:
    
    def test_pridat_ukol_positive(self, test_db_session):
        with patch('builtins.input', side_effect=['Test úkol', 'Test popis']):
            with patch('builtins.print'):
                result = pridat_ukol(test_db_session)
        
        assert result == True
        ukoly = test_db_session.query(Ukol).all()
        assert len(ukoly) == 1
        assert ukoly[0].nazev == 'Test úkol'
        assert ukoly[0].popis == 'Test popis'
        assert ukoly[0].stav == 'Nezahájeno'
    
    def test_pridat_ukol_negative_empty_input(self, test_db_session):
        with patch('builtins.input', side_effect=['', 'Test úkol', 'Test popis']):
            with patch('builtins.print'):
                result = pridat_ukol(test_db_session)
        
        assert result == True
        ukoly = test_db_session.query(Ukol).all()
        assert len(ukoly) == 1


class TestZobrazitUkoly:
    
    def test_zobrazit_ukoly_positive(self, test_db_session):
        ukol1 = Ukol(nazev='Úkol 1', popis='Popis 1', stav='Nezahájeno', datum_vytvoreni=datetime.now())
        ukol2 = Ukol(nazev='Úkol 2', popis='Popis 2', stav='Probíhá', datum_vytvoreni=datetime.now())
        test_db_session.add_all([ukol1, ukol2])
        test_db_session.commit()
        
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            zobrazit_ukoly(test_db_session)
        
        output = captured_output.getvalue()
        assert 'Úkol 1' in output
        assert 'Úkol 2' in output
        assert 'Nezahájeno' in output
        assert 'Probíhá' in output
    
    def test_zobrazit_ukoly_negative_empty_list(self, test_db_session):
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            zobrazit_ukoly(test_db_session)
        
        output = captured_output.getvalue()
        assert 'prázdný' in output.lower()


class TestAktualizovatUkol:
    
    def test_aktualizovat_ukol_positive(self, test_db_session):
        ukol = Ukol(nazev='Úkol k aktualizaci', popis='Popis', stav='Nezahájeno', datum_vytvoreni=datetime.now())
        test_db_session.add(ukol)
        test_db_session.commit()
        
        with patch('builtins.input', side_effect=[str(ukol.id), '1']):
            with patch('builtins.print'):
                result = aktualizovat_ukol(test_db_session)
        
        assert result == True
        updated_ukol = test_db_session.query(Ukol).filter_by(id=ukol.id).first()
        assert updated_ukol.stav == 'Probíhá'
    
    def test_aktualizovat_ukol_negative_nonexistent_id(self, test_db_session):
        with patch('builtins.input', side_effect=['999', '1']):
            with patch('builtins.print') as mock_print:
                result = aktualizovat_ukol(test_db_session)
        
        assert result == False


class TestOdstranItUkol:
    
    def test_odstranit_ukol_positive(self, test_db_session):
        ukol = Ukol(nazev='Úkol k odstranění', popis='Popis', stav='Nezahájeno', datum_vytvoreni=datetime.now())
        test_db_session.add(ukol)
        test_db_session.commit()
        ukol_id = ukol.id
        
        with patch('builtins.input', side_effect=[str(ukol_id), 'ano']):
            with patch('builtins.print'):
                result = odstranit_ukol(test_db_session)
        
        assert result == True
        deleted_ukol = test_db_session.query(Ukol).filter_by(id=ukol_id).first()
        assert deleted_ukol is None
    
    def test_odstranit_ukol_negative_empty_list(self, test_db_session):
        with patch('builtins.input', side_effect=[]):
            with patch('builtins.print'):
                result = odstranit_ukol(test_db_session)
        
        assert result == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
