"""
Configuration file for database connection.
You can switch between different databases by changing the DATABASE_TYPE.
"""

# Database configuration
# Podporovane databazove servery 'mysql', 'postgresql', 'mssql', 'sqlite'
DATABASE_TYPE = 'mysql'  # Default je nastaveny na mysql, ale muzete zmenit na 'postgresql', 'mssql' nebo 'sqlite' podle potreby

# Databazove konfigurace pro ruzne typy databazi
DB_CONFIG = {
    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Czclone1998',
        'database': 'task_manager_db'
    },
    'postgresql': {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'your_password',
        'database': 'task_manager_db'
    },
    'mssql': {
        'host': 'localhost',
        'port': 1433,
        'user': 'sa',
        'password': 'your_password',
        'database': 'task_manager_db'
    },
    'sqlite': {
        'database': 'task_manager.db'  # sobor pro SQLite databazi
    }
}

# teastovaci databazova konfigurace pro jednotkove testy
TEST_DB_CONFIG = {
    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Czclone1998',
        'database': 'task_manager_test_db'
    },
    'postgresql': {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'your_password',
        'database': 'task_manager_test_db'
    },
    'mssql': {
        'host': 'localhost',
        'port': 1433,
        'user': 'sa',
        'password': 'your_password',
        'database': 'task_manager_test_db'
    },
    'sqlite': {
        'database': 'task_manager_test.db'
    }
}
