DATABASE_TYPE = 'mysql'
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
        'database': 'task_manager.db'
    }
}
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
