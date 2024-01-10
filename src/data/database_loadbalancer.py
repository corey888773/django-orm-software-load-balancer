from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import Base


class DatabaseLoadBalancer:
    def __init__(self, db_urls : List[str]):
        self.engines = {f'database{index}': create_engine(db_url) for index, db_url in enumerate(db_urls)}
        self.sessions = {f'database{index}': sessionmaker(bind=engine, autocommit=False, autoflush=False) for index, engine in enumerate(self.engines.values())}

    def migrate(self, model):
        for engine in self.engines.values():
            model.Base.metadata.create_all(bind=engine)

    def get_session_makers(self):
        return self.sessions['database0']

