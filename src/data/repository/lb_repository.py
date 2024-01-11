from .abstractions import ReadRepositoryInterface, WriteRepositoryInterface, LoadBalancingStrategyInterface
from .lb_strategy import RoundRobinStrategy
from ..database import DatabaseWrapper
from ..events import *
from ..models.todo_item import TodoItem
from schemas import TodoItemSchema, Response


class LoadBalancerReadRepository(ReadRepositoryInterface):
    def __init__(self, dbws: list[DatabaseWrapper], default_strategy: LoadBalancingStrategyInterface=RoundRobinStrategy()):
        self.db_wrapper = {dbw.get_id(): dbw for dbw in dbws}
        self.strategy = default_strategy

    def list_todo_items(self) -> list[TodoItem]:
        dbw = self.strategy.choose(self.db_wrapper.values())
        if dbw.is_connected():
            with dbw.make_session() as db:
                return db.query(TodoItem).all()

    def get_todo_item_by_id(self, id: int) -> TodoItem:
        dbw = self.strategy.choose(self.db_wrapper.values())
        if dbw.is_connected():
            with dbw.make_session() as db:
                return db.query(TodoItem).filter(TodoItem.id == id).first()


class LoadBalancerWriteRepository(WriteRepositoryInterface):
    def __init__(self, dbws: list[DatabaseWrapper]):
        self.db_wrapper = {dbw.get_id(): dbw for dbw in dbws}

    def create_todo_item(self, todo_item: TodoItemSchema) -> TodoItem:
        event = TodoItemCreatedEvent(title=todo_item.title, description=todo_item.description, completed=todo_item.completed)
        for _, dbw in self.db_wrapper.items():
            dbw.register_event(event)
        
            if dbw.is_connected():
                dbw.commit_events()

    def update_todo_item(self, id: int, todo_item: TodoItemSchema) -> TodoItem:
        event = TodoItemUpdatedEvent(id=id, title=todo_item.title, description=todo_item.description, completed=todo_item.completed)
        for _, dbw in self.db_wrapper.items():
            dbw.register_event(event)
        
            if dbw.is_connected():
                dbw.commit_events()

    def delete_todo_item(self, id: int) -> Response:
        event = TodoItemDeletedEvent(id=id)
        for _, dbw in self.db_wrapper.items():
            dbw.register_event(event)
        
            if dbw.is_connected():
                dbw.commit_events()