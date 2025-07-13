from config import BACKEND_URL
from repositories.api_respository import APIRepository
from repositories.sqllite_repository import SQLiteRepository
from core.interfaces import IJobRepository

def get_repository() -> IJobRepository:
    if BACKEND_URL:
        return APIRepository()
    else:
        return SQLiteRepository()
