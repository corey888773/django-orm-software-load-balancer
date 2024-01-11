import abc
from ..models.todo_item import TodoItem
from schemas import RequestTodoItem, Response
from ..database import DatabaseWrapper

# repository pattern http://www.pzielinski.com/?p=281

class ReadRepositoryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def list_todo_items(self) -> list[TodoItem]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_todo_item_by_id(self, id: int) -> TodoItem:
        raise NotImplementedError


class WriteRepositoryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def create_todo_item(self, todo_item: RequestTodoItem) -> TodoItem:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_todo_item(self, id: int, todo_item: RequestTodoItem) -> TodoItem:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_todo_item(self, id: int) -> Response:
        raise NotImplementedError


# TODO: Implement UnitOfWork logic
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


class LoadBalancingStrategyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def choose(self, databases: list[DatabaseWrapper]) -> DatabaseWrapper:
        raise NotImplementedError
