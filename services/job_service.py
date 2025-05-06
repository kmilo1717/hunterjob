from database.database import Database
from config import FILTERS, BACKEND_URL
import requests

class JobService:
    def __init__(self):
        self.db = Database()
    def get_vacancies(self):
        salary = int(FILTERS.get('MIN_SALARY', 0))
        modalities = FILTERS.get('MODALITY')

        if BACKEND_URL:
            # Construir los filtros como query params para el backend
            params = {
                "status": "pending",
            }
            if salary > 0:
                params["min_salary"] = salary
            if modalities:
                params["modalities"] = ','.join(modalities)

            response = requests.get(f"{BACKEND_URL}/jobs", params=params)
            return response.json() if response.status_code == 200 else []

        query = "SELECT * FROM jobs WHERE status = 'pending'"
        values = []

        if salary > 0:
            query += " AND (salary_int = 0 OR salary_int >= ?)"
            values.append(salary)

        if modalities:
            placeholders = ','.join('?' for _ in modalities)
            query += f" AND modality IN ({placeholders})"
            values.extend(modalities)

        return self.db.fetch_all("jobs", query, tuple(values))

    def apply_job(self, status, job_id):
        if BACKEND_URL:
            response = requests.put(f"{BACKEND_URL}/jobs/{job_id}", json={"status": status})
            return response.status_code == 204
        self.db.execute_query("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
        return True