from database.database import Database
from core.interfaces import IService
from utils.utils import setup_logger
from models.job import Job
import json
from config import COOKIE_UCA
class ComputrabajoService(IService):
    def __init__(self):
        self.db = Database()
        self.logger = setup_logger(__name__)
        self.context = "computrabajo"
    
    def create_job(self, title, url, company, job_id, salary, contract_type, schedule, modality, description, location, status = 'pending', salary_int = 0):
        job = Job(title, url, company, job_id, salary, contract_type, schedule, modality, description, location, status, salary_int)
        job.save()
        return job
    
    def load_cookies(self, driver, include_only=[]):
        try:
            file_path="cookies.json"
            with open(file_path, "r") as file:
                cookies = json.load(file)
            for cookie in cookies[self.context]:
                if include_only and cookie['name'] not in include_only:
                    continue
                if cookie['name'] == 'uca':
                    cookie['value'] = COOKIE_UCA
                driver.add_cookie(cookie)
            print("Cookies cargadas.")
        except FileNotFoundError:
            print("No se encontraron cookies.")
            self.logger.error("No se encontraron cookies.")