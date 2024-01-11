import abc
from ..models.todo_item import TodoItem
from schemas import RequestTodoItem, Response

class ReadRepositoryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_todo_items(self) -> list[TodoItem]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_todo_item_by_id(self, id: int) -> TodoItem:
        raise NotImplementedError

class WriteRepositoryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_todo_item(self, todo_item: RequestTodoItem) -> TodoItem:
        raise NotImplementedError

    @abc.abstractmethod
    def update_todo_item(self, id: int, todo_item: RequestTodoItem) -> TodoItem:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_todo_item(self, id: int) -> Response:
        raise NotImplementedError


class LoadBalancingStrategyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def choose(self, servers: list) -> str:
        raise NotImplementedError