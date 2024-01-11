from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import Base
from .database import DatabaseWrapper

class LoadBalancer:
    def __init__(self):
        self.dbs: Dict[str, DatabaseWrapper] = {}

    def register(self, db: DatabaseWrapper):
        self.dbs[db.get_id()] = db

    def get_session_makers(self):
        return [db.get_session_maker() for db in self.dbs.values()]

    def get_db(self, id: str) -> DatabaseWrapper:
        return self.dbs[id]

    def get_dbs(self) -> List[DatabaseWrapper]:
        return list(self.dbs.values())
