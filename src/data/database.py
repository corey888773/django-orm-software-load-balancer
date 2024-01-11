from sqlalchemy import create_engine, text
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
        try:
            with self.engine.connect() as conn:
                conn.execute(text('select 1'))
            print(f'Database {self.id} is connected')
        except Exception as e:
            print(f'Database {self.id} is not connected')
            return False
        return True

    def is_synced(self):
        return len(self.event_queue) == 0

    def commit_events(self):
        while not self.is_synced():
            try:
                event = self.event_queue.pop(0)
                print(f'Publishing event {event}')
                self.events_mediator.handle(event)
                print(f'Event {event} published')
            except Exception as e:
                print(f'Error publishing event {e}')
                break

    @contextmanager
    def make_session(self):
        session = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()


