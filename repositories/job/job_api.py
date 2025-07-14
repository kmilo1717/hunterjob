import requests
from config import BACKEND_URL, FILTERS
from core.interfaces import IJobDataSource

class JobApi(IJobDataSource):
    def get_vacancies(self, salary=0, modalities=None, schedules=None):
        params = {"status": "pending"}
        params["salary"] = salary
        if schedules:
            params["schedules"] = ','.join(schedules)
        for modality, min_salary in modalities:
            params[modality] = min_salary

        response = requests.get(f"{BACKEND_URL}/jobs", params=params)
        return response.json() if response.status_code == 200 else []

    def apply_job(self, status, job_id):
        response = requests.put(f"{BACKEND_URL}/jobs/{job_id}", json={"status": status})
        return response.status_code == 204