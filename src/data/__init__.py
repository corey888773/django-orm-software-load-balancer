from .config import DATABASE_URLS
from .loadbalancer import LoadBalancer
from . import models
from .repository import TodoItemRepository
from .database import DatabaseWrapper
from .unitofwork import UnitOfWork

db_load_balancer = LoadBalancer()

for idx, url in enumerate(DATABASE_URLS):
    database = DatabaseWrapper(conn_str=url, id=f'database{idx+1}')
    database.migrate(models.todo_item)
    db_load_balancer.register(database)

databases = db_load_balancer.get_dbs()
todo_repository = [TodoItemRepository(dbw=dbw) for dbw in databases]
unit_of_work = UnitOfWork(None)

__all__ = [
    'db_load_balancer',
    'todo_repository'
]
