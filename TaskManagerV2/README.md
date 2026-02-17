# Task Manager V2 - Dokumentace

## Přehled projektu

Task Manager je aplikace pro správu úkolů s podporou databáze. Program umožňuje vytvářet, zobrazovat, aktualizovat a mazat úkoly (CRUD operace) s ukládáním do databáze.

### Hlavní vlastnosti:
- ✅ Podpora více typů databází (MySQL, PostgreSQL, MSSQL, SQLite)
- ✅ CRUD operace (Create, Read, Update, Delete)
- ✅ Automatické testování pomocí pytest
- ✅ Čistá architektura s oddělením logiky
- ✅ Validace vstupů
- ✅ Filtrace úkolů podle stavu

---

## Struktura projektu

```
TaskManagerV2/
│
├── main.py                  # Hlavní soubor programu (spouštění)
├── database.py              # Databázové operace a modely
├── task_operations.py       # CRUD funkce pro úkoly
├── config.py                # Konfigurace databáze
├── test_task_manager.py     # Automatizované testy
├── requirements.txt         # Python závislosti
└── README.md                # Tato dokumentace
```

---

## Instalace a nastavení

### 1. Instalace závislostí

```bash
# Aktivace virtuálního prostředí (pokud používáte)
python -m venv .venv
source .venv/bin/activate  # Na macOS/Linux
# nebo
.venv\Scripts\activate  # Na Windows

# Instalace základních balíčků
pip install SQLAlchemy pytest

# Pro SQLite (výchozí) - není potřeba nic dalšího

# Pro MySQL
pip install PyMySQL

# Pro PostgreSQL
pip install psycopg2-binary

# Pro MSSQL
pip install pyodbc
```

Nebo nainstalujte všechny závislosti najednou:
```bash
pip install -r requirements.txt
```

### 2. Konfigurace databáze

Otevřete soubor `config.py` a nastavte:

```python
# Výběr typu databáze
DATABASE_TYPE = 'mysql'  # 'mysql', 'postgresql', 'mssql', 'sqlite'

# Nastavení přístupových údajů (příklad pro MySQL)
DB_CONFIG = {
    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'vase_heslo',
        'database': 'task_manager_db'
    },
    # ... další konfigurace
}
```

#### Doporučení pro začátečníky:
- **SQLite**: Nejjednodušší volba, nevyžaduje instalaci serveru
- **MySQL**: Populární, snadno se instaluje přes XAMPP nebo Docker
- **PostgreSQL**: Pokročilejší, robustní řešení
- **MSSQL**: Pro Windows prostředí

### 3. Vytvoření databáze (pro MySQL/PostgreSQL/MSSQL)

Pokud nepoužíváte SQLite, musíte nejprve vytvořit databázi:

**MySQL:**
```sql
CREATE DATABASE task_manager_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE task_manager_test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**PostgreSQL:**
```sql
CREATE DATABASE task_manager_db;
CREATE DATABASE task_manager_test_db;
```

Tabulky se vytvoří automaticky při prvním spuštění programu.

---

## Spuštění programu

```bash
python main.py
```

Program se automaticky:
1. Připojí k databázi
2. Vytvoří tabulku `ukoly`, pokud neexistuje
3. Zobrazí hlavní menu

---

## Použití aplikace

### Hlavní menu

```
==================================================
        TASK MANAGER - Správce úkolů
==================================================
1. Přidat úkol
2. Zobrazit úkoly
3. Aktualizovat úkol
4. Odstranit úkol
5. Ukončit program
==================================================
```

### 1. Přidání úkolu
- Zadejte název úkolu (povinné)
- Zadejte popis úkolu (povinné)
- Úkol se automaticky uloží se stavem "Nezahájeno"

### 2. Zobrazení úkolů
- Zobrazí všechny úkoly se stavem "Nezahájeno" nebo "Probíhá"
- Dokončené úkoly se nezobrazují

### 3. Aktualizace úkolu
- Vyberte úkol podle ID
- Změňte stav na:
  - "Probíhá" - úkol probíhá
  - "Hotovo" - úkol je dokončen

### 4. Odstranění úkolu
- Vyberte úkol podle ID
- Potvrďte odstranění
- Úkol bude trvale smazán

---

## Testování

### Spuštění testů

```bash
# Spustit všechny testy
pytest test_task_manager.py -v

# Spustit s pokrytím kódu
pytest test_task_manager.py --cov=. --cov-report=html

# Spustit konkrétní test
pytest test_task_manager.py::TestPridatUkol::test_pridat_ukol_pozitivni -v
```

### Testovací případy

Program obsahuje 11 testovacích případů:

#### Testy přidání úkolu (3 testy)
- TC01: Přidání úkolu s platnými daty ✅
- TC02: Pokus o přidání s prázdným názvem ❌
- TC03: Pokus o přidání s prázdným popisem ❌

#### Testy aktualizace (3 testy)
- TC04: Změna stavu na "Probíhá" ✅
- TC05: Aktualizace neexistujícího úkolu ❌
- TC06: Změna stavu na "Hotovo" ✅

#### Testy odstranění (2 testy)
- TC07: Odstranění existujícího úkolu ✅
- TC08: Odstranění neexistujícího úkolu ❌

#### Testy zobrazení (2 testy)
- TC09: Zobrazení s filtrem stavu ✅
- TC10: Zobrazení prázdného seznamu ✅

#### Komplexní test (1 test)
- TC11: Kompletní CRUD cyklus ✅

### Testovací databáze

Testy používají samostatnou testovací databázi (definovanou v `config.py`):
- Pro SQLite: `task_manager_test.db`
- Pro ostatní: `task_manager_test_db`

Testovací data se automaticky vytvoří před testem a smažou po testu.

---

## Struktura databáze

### Tabulka: `ukoly`

| Sloupec          | Typ          | Popis                                    |
|------------------|--------------|------------------------------------------|
| id               | INTEGER      | Primární klíč (auto-increment)           |
| nazev            | VARCHAR(200) | Název úkolu (povinné)                    |
| popis            | VARCHAR(500) | Popis úkolu (povinné)                    |
| stav             | VARCHAR(50)  | Stav: "Nezahájeno", "Probíhá", "Hotovo" |
| datum_vytvoreni  | DATETIME     | Automaticky při vytvoření                |

---

## Příklady použití kódu

### Přidání úkolu programově

```python
from database import pripojeni_db, vytvoreni_tabulky, Ukol
from datetime import datetime

# Připojení
engine, Session = pripojeni_db()
vytvoreni_tabulky(engine)
session = Session()

# Přidání úkolu
novy_ukol = Ukol(
    nazev="Naučit se Python",
    popis="Projít kurz SQLAlchemy",
    stav="Nezahájeno",
    datum_vytvoreni=datetime.now()
)
session.add(novy_ukol)
session.commit()

session.close()
```

### Dotaz na úkoly

```python
# Všechny aktivní úkoly
aktivni = session.query(Ukol).filter(
    Ukol.stav.in_(['Nezahájeno', 'Probíhá'])
).all()

# Úkol podle ID
ukol = session.query(Ukol).filter_by(id=1).first()

# Dokončené úkoly
dokoncene = session.query(Ukol).filter_by(stav='Hotovo').all()
```

---

## Řešení problémů

### Chyba: "No module named 'pymysql'"
```bash
pip install PyMySQL
```

### Chyba: "Access denied for user"
- Zkontrolujte přístupové údaje v `config.py`
- Ověřte, že databáze existuje
- Zkontrolujte práva uživatele

### Chyba: "Table doesn't exist"
- Program automaticky vytvoří tabulky při prvním spuštění
- Pokud problém přetrvává, smažte databázi a spusťte znovu

### SQLite: "database is locked"
- Zavřete všechny spojení k databázi
- Ujistěte se, že voláte `session.close()`

---

## Doporučení pro pokročilejší použití

### 1. Migrace databází
Pro správu změn schématu databáze použijte **Alembic**:
```bash
pip install alembic
alembic init alembic
```

### 2. Prostředí variables
Místo ukládání hesel v `config.py` použijte `.env`:
```bash
pip install python-dotenv
```

### 3. Docker pro databáze
Rychlé spuštění MySQL v Dockeru:
```bash
docker run --name mysql-taskmanager -e MYSQL_ROOT_PASSWORD=heslo -p 3306:3306 -d mysql:8.0
```

---

## Výhody použití SQLAlchemy

1. **Abstrakce databáze**: Jeden kód funguje pro všechny databáze
2. **ORM**: Práce s objekty místo SQL příkazů
3. **Bezpečnost**: Automatická ochrana proti SQL injection
4. **Migrace**: Snadné změny schématu databáze
5. **Produktivita**: Méně kódu, více funkcí

---

## Autor a licence

Tento projekt byl vytvořen jako školní úkol pro výuku práce s databázemi v Pythonu.

**Použité technologie:**
- Python 3.8+
- SQLAlchemy 2.0+
- pytest
- PyMySQL / psycopg2 / pyodbc

---

## Kontakt a podpora

Pokud máte dotazy nebo narazíte na problém:
1. Zkontrolujte sekci "Řešení problémů"
2. Ověřte konfiguraci v `config.py`
3. Spusťte testy pro ověření funkčnosti

---

**Hodně štěstí s projektem! 🚀**
