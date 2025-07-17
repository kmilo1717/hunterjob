import requests
from config import BACKEND_URL
from core.interfaces import IRepository

class APIRepository(IRepository):
    def insert_one(self, table, params):
        if 'job_id' in params:
            params['jobId'] = params.pop('job_id')
            params['contractType'] = params.pop('contract_type')
            params['salaryInt'] = params.pop('salary_int')
        response = requests.post(f"{BACKEND_URL}/{table}", json=params)
        return response.json() if response.status_code == 201 else None

    def fetch_all(self, table):
        response = requests.get(f"{BACKEND_URL}/{table}")
        return response.json() if response.status_code == 200 else []

    def fetch_one(self, table, query=None, params=None):
        if not params or 'id' not in params:
            raise ValueError("Falta parámetro 'id'")
        response = requests.get(f"{BACKEND_URL}/{table}/{params['id']}")
        return response.json() if response.status_code == 200 else None

    def update_one(self, table, query=None, params=None):
        response = requests.put(f"{BACKEND_URL}/{table}/{params['id']}", json=params)
        return response.status_code == 200
