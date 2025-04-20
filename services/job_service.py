from database.database import Database
from config import FILTERS

class JobService:
    def __init__(self):
        self.db = Database()
    def get_vacancies(self):
        salary = int(FILTERS.get('MIN_SALARY', 0))
        modalities = FILTERS.get('MODALITY')

        query = "SELECT * FROM jobs WHERE status = 'pending'"
        params = []

        if salary > 0:
            query += " AND (salary_int = 0 OR salary_int >= ?)"
            params.append(salary)

        if modalities:
            placeholders = ','.join('?' for _ in modalities)
            query += f" AND modality IN ({placeholders})"
            params.extend(modalities)

        return [job for job in self.db.fetch_all(query, tuple(params))]

    def apply_job(self, status, job_id):
        self.db.execute_query("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
        return True