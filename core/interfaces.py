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