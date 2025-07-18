from repositories.job.job_api import JobApi
from repositories.job.job_repository import JobRepository
from config import BACKEND_URL
from database.database import Database
class JobService:
    def __init__(self):
        db = Database() if not BACKEND_URL else None
        self.data_source = JobApi() if BACKEND_URL else JobRepository(db)

    def get_vacancies(self, modalities=None, schedules=None):
        return self.data_source.get_vacancies(modalities, schedules)

    def apply_job(self, status, job_id):
        return self.data_source.apply_job(status, job_id)
