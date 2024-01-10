import abc
from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
from typing import List, Type
from .models.todo_item import TodoItem

class EventInterface(metaclass=abc.ABCMeta):
    pass

class EventHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, event: EventInterface):
        raise NotImplementedError

class TodoItemRepositoryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_todo_items(self, db: Session) -> list[Type[TodoItem]]:
        pass

    @abc.abstractmethod
    def get_todo_item_by_id(self, db: Session, id: int) -> TodoItem:
        pass

    @abc.abstractmethod
    def create_todo_item(self, db: Session, todo_item: RequestTodoItem) -> TodoItem:
        pass

    @abc.abstractmethod
    def update_todo_item(self, db: Session, id: int, todo_item: RequestTodoItem) -> TodoItem:
        pass

    @abc.abstractmethod
    def delete_todo_item(self, db: Session, id: int) -> Response:
        pass


class UnitOfWorkInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self):
        raise NotImplementedError
