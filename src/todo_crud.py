from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
from typing import List, Type

from models.todo_item import TodoItem


def list_todo_items(db: Session) -> list[Type[TodoItem]]:
    return db.query(TodoItem).all()


def get_todo_item_by_id(db: Session, id: int) -> TodoItem:
    return db.query(TodoItem).filter(TodoItem.id == id).first()


def create_todo_item(db: Session, todo_item: RequestTodoItem) -> TodoItem:
    _todo_item = TodoItem(title=todo_item.parameter.title, description=todo_item.parameter.description, completed=todo_item.parameter.completed)
    db.add(_todo_item)
    db.commit()
    db.refresh(_todo_item)
    return _todo_item


def update_todo_item(db: Session, id: int, todo_item: RequestTodoItem) -> TodoItem: 
    _todo_item = db.query(TodoItem).filter(TodoItem.id == id).first()
    _todo_item.title = todo_item.parameter.title
    _todo_item.description = todo_item.parameter.description
    _todo_item.completed = todo_item.parameter.completed
    db.commit()
    db.refresh(_todo_item)
    return _todo_item


def delete_todo_item(db: Session, id: int) -> Response:
    _todo_item = db.query(TodoItem).filter(TodoItem.id == id).first()
    db.delete(_todo_item)
    db.commit()
    return Response(code="200", status="OK", message="Todo Item Deleted", result=None)