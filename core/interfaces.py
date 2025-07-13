from abc import ABC, abstractmethod

class IScraper(ABC):
    @abstractmethod
    def scrape(self, keywords):
        pass

class IApplicator(ABC):
    @abstractmethod
    def apply(self):
        pass

class IService(ABC):
    @abstractmethod
    def load_cookies(self, driver, include_only=[]):
        pass

class IJobDataSource(ABC):
    @abstractmethod
    def get_vacancies(self, salary=0, modalities=None):
        pass

    @abstractmethod
    def apply_job(self, status, job_id):
        pass

class IRepository(ABC):
    @abstractmethod
    def insert_one(self, table, params):
        pass

    @abstractmethod
    def fetch_all(self, table):
        pass

    @abstractmethod
    def fetch_one(self, table, query=None, params=None):
        pass

    @abstractmethod
    def update_one(self, table, query, params=None):
        pass

class ISQLiteRepository(IRepository):
    @abstractmethod
    def execute_query(self, query, params=None):
        pass

