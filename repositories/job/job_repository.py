from core.interfaces import IJobDataSource

class JobRepository(IJobDataSource):
    def __init__(self, db):
        self.db = db

    def get_vacancies(self, salary=0, modalities=None, schedules=None):
        query = "SELECT * FROM jobs WHERE status = 'pending'"
        values = []

        if salary > 0:
            query += " AND (salary_int = 0 OR salary_int >= ?)"
            values.append(salary)

        if modalities:
            placeholders = ','.join('?' for _ in modalities)
            query += f" AND modality IN ({placeholders})"
            values.extend(modalities)
        
        if schedules:
            placeholders = ','.join('?' for _ in schedules)
            query += f" AND schedule IN ({placeholders})"
            values.extend(schedules)

        return self.db.fetch_all("jobs", query, tuple(values))

    def apply_job(self, status, job_id):
        self.db.execute_query("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
        return True
