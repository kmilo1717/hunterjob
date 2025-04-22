import sqlite3
from config import DB_NAME
import os

class Database:
    _instance = None
    _connection = None

    def __new__(cls, db_name=DB_NAME):
        if not cls._instance:
            if not os.path.exists('data'):
                os.makedirs('data')
            cls._instance = super().__new__(cls)
            cls._connection = sqlite3.connect('data/' + db_name)
            cls._connection.row_factory = sqlite3.Row
        return cls._instance

    @staticmethod
    def get_connection():
        if not Database._instance:
            Database()
        return Database._connection

    def execute_query(self, query, params=None):
        cursor = self.get_connection().cursor()
        cursor.execute(query, params or ())
        self.get_connection().commit()
        return cursor
    def insert_one(self, table, params=None): 
        if not params:
            raise ValueError("No se proporcionaron parámetros para insertar.")
        columns = ', '.join(params.keys())
        placeholders = ', '.join('?' for _ in params)
        values = tuple(params.values())
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.get_connection().cursor()
        cursor.execute(query, values)
        self.get_connection().commit()
        return cursor
    def fetch_all(self, query, params=None):
        cursor = self.get_connection().cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        cursor = self.get_connection().cursor()
        cursor.execute(query, params or ())
        return cursor.fetchone()

    def close(self):
        if Database._connection:
            Database._connection.close()
            Database._connection = None
