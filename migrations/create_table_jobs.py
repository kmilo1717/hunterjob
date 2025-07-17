from repositories.factory import get_repository
def create_table_jobs():
    repo = get_repository()
    repo.execute_query("""
        CREATE TABLE IF NOT EXISTS "jobs" (
            "id"	INTEGER,
            "title"	TEXT,
            "url"	TEXT,
            "company"	TEXT,
            "job_id"	TEXT UNIQUE,
            "salary"	TEXT,
            "contract_type"	TEXT,
            "schedule"	TEXT,
            "modality"	TEXT,
            "description"	TEXT,
            "location"	TEXT,
            "status"	TEXT,
            "created_at"	TEXT DEFAULT (datetime('now')),
            "salary_int"	INTEGER DEFAULT 0,
            PRIMARY KEY("id" AUTOINCREMENT)
        );  
    """)