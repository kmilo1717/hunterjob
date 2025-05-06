import sqlite3
from config import DB_NAME, BACKEND_URL
import os
import requests

class Database:
    _instance = None
    _connection = None
    _url = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            if not BACKEND_URL:
                if not os.path.exists('data'):
                    os.makedirs('data')
                cls._connection = sqlite3.connect('data/' + DB_NAME)
                cls._connection.row_factory = sqlite3.Row
        cls._url = BACKEND_URL if BACKEND_URL else None
        return cls._instance

    @staticmethod
    def get_connection():
        if BACKEND_URL:
            raise RuntimeError("Using backend API, not local DB")
        if not Database._instance:
            Database()
        return Database._connection

    def execute_query(self, query, params=None):
        if BACKEND_URL:
            raise NotImplementedError("execute_query is not supported when using BACKEND_URL")
        cursor = self.get_connection().cursor()
        cursor.execute(query, params or ())
        self.get_connection().commit()
        return cursor

    def insert_one(self, table, params=None): 
        if not params:
            raise ValueError("No se proporcionaron parámetros para insertar.")
        
        if BACKEND_URL:
            if 'job_id' in params:
                params['jobId'] = params.pop('job_id')
                params['contractType'] = params.pop('contract_type')
                params['salaryInt'] = params.pop('salary_int')
            response = requests.post(f"{self._url}/{table}", json=params)
            return response.json() if response.status_code == 201 else None

        columns = ', '.join(params.keys())
        placeholders = ', '.join('?' for _ in params)
        values = tuple(params.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.get_connection().cursor()
        cursor.execute(query, values)
        self.get_connection().commit()
        return cursor

    def fetch_all(self, table):
        if BACKEND_URL:
            response = requests.get(f"{self._url}/{table}")
            return response.json() if response.status_code == 200 else []
        
        cursor = self.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()

    def fetch_one(self, table, query=None, params=None):
        if BACKEND_URL:
            if not params or 'id' not in params:
                raise ValueError("Para usar el backend, debes pasar un parámetro 'id'")
            response = requests.get(f"{self._url}/{table}/{params['id']}")
            return response.json() if response.status_code == 200 else None

        cursor = self.get_connection().cursor()
        cursor.execute(query, params or ())
        return cursor.fetchone()
    
    def update_one(self, table, query, params=None):
        if BACKEND_URL:
            response = requests.put(f"{self._url}/{table}/{params['id']}", json=params)
            return True if response.status_code == 200 else False
        cursor = self.get_connection().cursor()
        cursor.execute(query, params or ())
        self.get_connection().commit()
        return cursor

    def close(self):
        if not BACKEND_URL and Database._connection:
            Database._connection.close()
            Database._connection = None
