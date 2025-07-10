from datasources.job_api import JobApi
from datasources.job_repository import JobRepository
from config import BACKEND_URL
from database.database import Database
class JobService:
    def __init__(self):
        db = Database() if not BACKEND_URL else None
        self.data_source = JobApi() if BACKEND_URL else JobRepository(db)

    def get_vacancies(self):
        return self.data_source.get_vacancies()

    def apply_job(self, status, job_id):
        return self.data_source.apply_job(status, job_id)
