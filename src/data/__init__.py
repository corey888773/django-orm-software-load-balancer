from .config import DATABASE_URLS
from .database_loadbalancer import DatabaseLoadBalancer
from . import models
from .repository import TodoItemRepository

db_load_balancer = DatabaseLoadBalancer(DATABASE_URLS)
db_load_balancer.migrate(models.todo_item)

sessionmaker = db_load_balancer.get_session_makers()
todo_repository = TodoItemRepository(sm=sessionmaker)


__all__ = [
    'db_load_balancer',
    'todo_repository'
]
