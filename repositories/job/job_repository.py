from core.interfaces import IJobDataSource

class JobRepository(IJobDataSource):
    def __init__(self, db):
        self.db = db

    def get_vacancies(self, modalities=None, schedules=None):
        query = "SELECT * FROM jobs WHERE status = 'pending'"
        values = []

        if modalities is None:
            modalities = {}

        if modalities:
            for modality, min_salary in modalities.items():
                query += "AND ((salary >= ? OR salary = 0) AND modality = ?)"
                values.append(min_salary)
                values.append(modality)
        
        if schedules:
            placeholders = ','.join('?' for _ in schedules)
            query += f" AND schedule IN ({placeholders})"
            values.extend(schedules)

        return self.db.fetch_all("jobs", query, tuple(values))

    def apply_job(self, status, job_id):
        self.db.execute_query("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
        return True
