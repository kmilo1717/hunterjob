import requests
from config import BACKEND_URL, FILTERS
from core.interfaces import IJobDataSource

class JobApi(IJobDataSource):
    def get_vacancies(self):
        params = {"status": "pending"}
        for modality, min_salary in FILTERS.items():
            params[modality] = min_salary

        response = requests.get(f"{BACKEND_URL}/jobs", params=params)
        return response.json() if response.status_code == 200 else []

    def apply_job(self, status, job_id):
        response = requests.put(f"{BACKEND_URL}/jobs/{job_id}", json={"status": status})
        return response.status_code == 204