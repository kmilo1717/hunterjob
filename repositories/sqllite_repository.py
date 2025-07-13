import sqlite3
import os
from config import DB_NAME
from core.interfaces import ISQLiteRepository

class SQLiteRepository(ISQLiteRepository):
    def __init__(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.conn = sqlite3.connect('data/' + DB_NAME)
        self.conn.row_factory = sqlite3.Row

    def insert_one(self, table, params):
        columns = ', '.join(params.keys())
        placeholders = ', '.join('?' for _ in params)
        values = tuple(params.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        return cursor

    def fetch_all(self, table):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()

    def fetch_one(self, query=None, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchone()

    def update_one(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        self.conn.commit()
        return cursor
    
    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        self.conn.commit()
        return cursor

    def close(self):
        self.conn.close()
