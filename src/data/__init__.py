from .config import DATABASE_URLS
from .loadbalancer import LoadBalancer
from . import models
from .repository import TodoItemRepository
from .database import DatabaseWrapper
from .unitofwork import UnitOfWork
from .events import *

db_load_balancer = LoadBalancer()

for idx, url in enumerate(DATABASE_URLS):
    database = DatabaseWrapper(conn_str=url, id=f'database{idx+1}')
    database.migrate(models.todo_item)
    db_load_balancer.register(database)

databases = db_load_balancer.get_dbs()
todo_repositories = [TodoItemRepository(dbw=dbw) for dbw in databases]
events_repositories = [EventsTodoItemRepository(dbw=dbw) for dbw in databases]
unit_of_work = UnitOfWork(None)

for dbw, repository in zip(databases, todo_repositories):
    dbw.events_mediator = EventsMediatorFactory.create(repository=repository, unit_of_work=unit_of_work)

__all__ = [
    'db_load_balancer',
    'todo_repositories',
    'unit_of_work'
]
