import abc
from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
from typing import List, Type
from .models.todo_item import TodoItem

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
