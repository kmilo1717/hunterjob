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