import sqlite3
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME')

class Database:
    _instance = None
    _connection = None

    def __new__(cls, db_name=DB_NAME):
        if not cls._instance:
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
