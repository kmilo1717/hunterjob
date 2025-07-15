import requests
from config import BACKEND_URL
from core.interfaces import IJobDataSource

class JobApi(IJobDataSource):
    def get_vacancies(self, modalities=None, schedules=None):
        if modalities is None:
            modalities = {}
            
        params = {"status": "pending"}
        if schedules:
            params["schedules"] = ','.join(schedules)

        for modality, min_salary in modalities.items():
            params[modality] = min_salary

        response = requests.get(f"{BACKEND_URL}/jobs", params=params)
        print(response.url)
        return response.json() if response.status_code == 200 else []

    def apply_job(self, status, job_id):
        response = requests.put(f"{BACKEND_URL}/jobs/{job_id}", json={"status": status})
        return response.status_code == 204