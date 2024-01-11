import abc
from .abstractions import QueryInterface, QueryHandlerInterface, UnitOfWorkInterface, ReadRepositoryInterface
from dataclasses import dataclass

@dataclass
class ListTodoItemsQuery(QueryInterface):
    pass

@dataclass
class GetTodoItemByIdQuery(QueryInterface):
    id: int

class ListTodoItemsQueryHandler(QueryHandlerInterface):
    def __init__(self, repository: list[ReadRepositoryInterface]):
        self.repository = repository

    async def handle(self, query: QueryInterface):
        return await self.repository.list_todo_items()

class GetTodoItemByIdQueryHandler(QueryHandlerInterface):
    def __init__(self, repository: list[ReadRepositoryInterface]):
        self.repository = repository

    async def handle(self, query: QueryInterface):
        return await self.repository.get_todo_item_by_id(query.id)

class QueriesInvoker:
    def __init__(self):
        self.query_handlers : Dict[QueryInterface, QueryHandlerInterface] = {}

    def register(self, query: QueryInterface, query_handler: QueryHandlerInterface):
        self.query_handlers[query] = query_handler

    def execute(self, query: QueryInterface):
        return self.query_handlers[query.__class__].handle(query)


