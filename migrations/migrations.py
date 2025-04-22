from migrations.create_table_jobs import create_table_jobs
from database.database import Database

# Secuencia de migraciones
secuence = {
    "CreateTableJobs": create_table_jobs,
}

def migrations_handler():
    create_migrations_table()
    sync_migrations_table()

def create_migrations_table():
    """Crea la tabla de migraciones si no existe."""
    db = Database()
    db.execute_query("""
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY,
        migration_name TEXT NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

def sync_migrations_table():
    """Verifica si las migraciones ya han sido aplicadas y las ejecuta si es necesario."""
    db = Database()
    applied_migrations = db.fetch_all("SELECT migration_name FROM migrations")
    applied_migrations_set = set([migration['migration_name'] for migration in applied_migrations])

    for migration_name, migration_func in secuence.items():
        if migration_name not in applied_migrations_set:
            migration_func()
            db.execute_query("INSERT INTO migrations (migration_name) VALUES (?)", (migration_name,))
            print(f"Migración '{migration_name}' aplicada con éxito.")
