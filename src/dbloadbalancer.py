from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URLS
import models.todo_item

class DbObject:
    def __init__(self, db_url : str):
        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)

class DbLoadBalancer:
    def __init__(self, db_urls : List[str]):
        self.engines = {f'database{index}': create_engine(db_url) for index, db_url in enumerate(db_urls)}
        self.sessions = {f'database{index}': sessionmaker(bind=engine, autocommit=False, autoflush=False) for index, engine in enumerate(self.engines.values())}

    def migrate(self, model):
        for engine in self.engines.values():
            model.Base.metadata.create_all(bind=engine)

    def get_sessions(self):
        ss = self.sessions['database0']()
        try :
            yield ss

        finally:
            ss.close()


dbLoadBalancer = DbLoadBalancer(DATABASE_URLS)
dbLoadBalancer.migrate(models.todo_item)