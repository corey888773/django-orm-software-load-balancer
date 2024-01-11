from sqlalchemy.orm import Session
from schemas import TodoItemSchema, Response
from typing import List
import abc
from sqlalchemy.orm.session import sessionmaker
from ..database import DatabaseWrapper
from .abstractions import ReadRepositoryInterface, WriteRepositoryInterface
from ..models.todo_item import TodoItem

class DefaultReadRepository(ReadRepositoryInterface):
    def __init__(self, dbw: DatabaseWrapper):
        self.db_wrapper = dbw

    def list_todo_items(self) -> list[TodoItem]:
        with self.db_wrapper.make_session() as db:
            return db.query(TodoItem).all()

    def get_todo_item_by_id(self, id: int) -> TodoItem:
        with self.db_wrapper.make_session() as db:
            return db.query(TodoItem).filter(TodoItem.id == id).first()


class DefaultWriteRepository(WriteRepositoryInterface):
    def __init__(self, dbw: DatabaseWrapper):
        self.db_wrapper = dbw

    def create_todo_item(self, todo_item: TodoItemSchema) -> TodoItem:
        with self.db_wrapper.make_session() as db:
            _todo_item = TodoItem(title=todo_item.title, description=todo_item.description, completed=todo_item.completed)
            db.add(_todo_item)
            db.commit()
            db.refresh(_todo_item)
            return _todo_item

    def update_todo_item(self, id: int, todo_item: TodoItemSchema) -> TodoItem: 
        with self.db_wrapper.make_session() as db:
            _todo_item = db.query(TodoItem).filter(TodoItem.id == id).first()
            _todo_item.title = todo_item.title
            _todo_item.description = todo_item.description
            _todo_item.completed = todo_item.completed
            db.commit()
            db.refresh(_todo_item)
            return _todo_item

    def delete_todo_item(self, id: int) -> Response:
        with self.db_wrapper.make_session() as db:
            _todo_item = db.query(TodoItem).filter(TodoItem.id == id).first()
            db.delete(_todo_item)
            db.commit()
            return Response(code="200", status="OK", message="Todo Item Deleted", result=None)
