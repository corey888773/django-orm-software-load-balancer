from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

class DatabaseWrapper:
    def __init__(self, conn_str: str, id: str):
        self.id = id
        self.engine = create_engine(conn_str, connect_args={
            'connect_timeout': 5,
            'options': '-c statement_timeout=5000',            
        })
        self.sessionmaker = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.event_queue = []
        self._events_mediator = None

    @property
    def events_mediator(self):
        return self._events_mediator

    @events_mediator.setter
    def events_mediator(self, value):
        self._events_mediator = value

    def migrate(self, model):
        model.Base.metadata.create_all(bind=self.engine)

    def get_session_maker(self):
        return self.sessionmaker

    def get_id(self):
        return self.id

    def register_event(self, event):
        self.event_queue.append(event)

    def is_connected(self):
        return self.engine.test_connection()

    def is_synced(self):
        return len(self.event_queue) == 0

    def commit_events(self):
        pass

    @contextmanager
    def make_session(self):
        ss = self.sessionmaker()
        try:
            yield ss
        finally:
            ss.close()


