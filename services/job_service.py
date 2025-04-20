from database.database import Database
from config import MIN_SALARY

class JobService:
    def __init__(self):
        self.db = Database()
    def get_vacancies(self):
        salary = int(MIN_SALARY)
        if salary > 0:
            return [job for job in self.db.fetch_all("SELECT * FROM jobs WHERE status = 'pending' AND (salary_int = 0 OR salary_int >= ?)", (salary,))]
        return [job for job in self.db.fetch_all("SELECT * FROM jobs WHERE status = 'pending'")]

    def apply_job(self, status, job_id):
        self.db.execute_query("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
        return True