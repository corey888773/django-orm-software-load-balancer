from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
# from .abstractions import DatabaseGeneralInterface, DatabaseEventsInterface

class DatabaseWrapper:
    def __init__(self, conn_str: str, id: str):
        self.id = id
        self.engine = create_engine(conn_str, connect_args={
            'connect_timeout': 5,
            'options': '-c statement_timeout=5000',            
        })
        self.sessionmaker = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.event_queue = []
        self._events_dispatcher = None

    def migrate(self, model):
        model.Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def make_session(self):
        session = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()

    def get_id(self):
        return self.id

    @property
    def events_dispatcher(self):
        return self._events_dispatcher

    @events_dispatcher.setter
    def events_dispatcher(self, value):
        self._events_dispatcher = value

    def register_event(self, event):
        self.event_queue.append(event)

    async def is_connected(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text('select 1')) 
            self.id_print('Connected')
        except Exception as e:
            self.id_print('Not Connected')
            return False
        return True

    def is_synced(self):
        return len(self.event_queue) == 0

    async def commit_events(self):
        while not self.is_synced():
            try:
                event = self.event_queue.pop(0) # FIFO 
                result = await self.events_dispatcher.handle(event)
                if result is None or isinstance(result, Exception):
                    self.id_print(f'Handled event: {event} - somethin went wrong: {result}')
                else:
                    self.id_print(f'Handled event: {event} - with result: {result.__dict__}')

                # there might be a better way to handle errors like for example retrying, catching specific errors, etc.
            except Exception as ex:  
                self.id_print(f'Error publishing event {ex}')
                break

    def id_print(self, *args, **kwargs):
        print(f'Database {self.id}: ', *args, **kwargs)
