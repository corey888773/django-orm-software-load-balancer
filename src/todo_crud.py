from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
from typing import List, Type
import abc

from models.todo_item import TodoItem

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

class TodoItemRepository(TodoItemRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def list_todo_items(self) -> list[Type[TodoItem]]:
        return self.db.query(TodoItem).all()

    def get_todo_item_by_id(self, id: int) -> TodoItem:
        return self.db.query(TodoItem).filter(TodoItem.id == id).first()

    def create_todo_item(self, todo_item: RequestTodoItem) -> TodoItem:
        _todo_item = TodoItem(title=todo_item.parameter.title, description=todo_item.parameter.description, completed=todo_item.parameter.completed)
        self.db.add(_todo_item)
        self.db.commit()
        self.db.refresh(_todo_item)
        return _todo_item

    def update_todo_item(self, id: int, todo_item: RequestTodoItem) -> TodoItem: 
        _todo_item = self.db.query(TodoItem).filter(TodoItem.id == id).first()
        _todo_item.title = todo_item.parameter.title
        _todo_item.description = todo_item.parameter.description
        _todo_item.completed = todo_item.parameter.completed
        self.db.commit()
        self.db.refresh(_todo_item)
        return _todo_item

    def delete_todo_item(self, id: int) -> Response:
        _todo_item = self.db.query(TodoItem).filter(TodoItem.id == id).first()
        self.db.delete(_todo_item)
        self.db.commit()
        return Response(code="200", status="OK", message="Todo Item Deleted", result=None)