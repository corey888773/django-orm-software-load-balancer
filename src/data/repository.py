from sqlalchemy.orm import Session
from schemas import TodoItemSchema, Response
from typing import List, Type
import abc
from sqlalchemy.orm.session import sessionmaker
from .loadbalancer import LoadBalancer
from .database import DatabaseWrapper
from .events import *
from .abstractions import TodoItemRepositoryInterface

from .models.todo_item import TodoItem

class TodoItemRepository(TodoItemRepositoryInterface):
    def __init__(self, dbw: DatabaseWrapper):
        self.db_wrapper = dbw

    def list_todo_items(self) -> list[Type[TodoItem]]:
        with self.db_wrapper.make_session() as db:
            return db.query(TodoItem).all()

    def get_todo_item_by_id(self, id: int) -> TodoItem:
        with self.db_wrapper.make_session() as db:
            return db.query(TodoItem).filter(TodoItem.id == id).first()

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


class EventsTodoItemRepository(TodoItemRepositoryInterface):
    def __init__(self, dbw: DatabaseWrapper):
        self.db_wrapper = dbw

    def list_todo_items(self) -> list[Type[TodoItem]]:
        pass

    def get_todo_item_by_id(self, id: int) -> TodoItem:
        pass

    def create_todo_item(self, todo_item: TodoItemSchema) -> TodoItem:
        event = TodoItemCreatedEvent(title=todo_item.parameter.title, description=todo_item.parameter.description, completed=todo_item.parameter.completed)
        self.db_wrapper.register_event(event)

        if self.db_wrapper.is_connected():
            self.db_wrapper.commit_events()


    def update_todo_item(self, id: int, todo_item: TodoItemSchema) -> TodoItem:
        pass

    def delete_todo_item(self, id: int) -> Response:
        pass


class LbTodoItemRepository(TodoItemRepositoryInterface):
    def __init__(self, rps: List[TodoItemRepositoryInterface], lb : LoadBalancer):
        self.repostories = rps
        self.loadbalancer = lb

    def list_todo_items(self) -> list[Type[TodoItem]]:
        random = random.randint(0, len(self.repostories) - 1)

        return self.repostories[random].list_todo_items()

    def get_todo_item_by_id(self, id: int) -> TodoItem:
        random = random.randint(0, len(self.repostories) - 1)

        return self.repostories[random].get_todo_item_by_id(id=id)

    def create_todo_item(self, todo_item: TodoItemSchema) -> TodoItem:
        random = random.randint(0, len(self.repostories) - 1)

        return self.repostories[random].create_todo_item(todo_item=todo_item)

    def update_todo_item(self, id: int, todo_item: TodoItemSchema) -> TodoItem:
        random = random.randint(0, len(self.repostories) - 1)

        return self.repostories[random].update_todo_item(id=id, todo_item=todo_item)

    def delete_todo_item(self, id: int) -> Response:
        random = random.randint(0, len(self.repostories) - 1)

        return self.repostories[random].delete_todo_item(id=id)