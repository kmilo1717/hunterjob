from database.database import Database
class Job:
    def __init__(self, title, url, company, job_id, salary, contract_type, schedule, modality, description, location, status = 'pending', salary_int = 0):
        self.title = title
        self.url = url
        self.company = company
        self.job_id = job_id
        self.salary = salary
        self.contract_type = contract_type
        self.schedule = schedule
        self.modality = modality
        self.description = description
        self.location = location
        self.status = status
        self.salary_int = salary_int
    
    def save(self):
        Database().insert_one("jobs", self.__dict__)