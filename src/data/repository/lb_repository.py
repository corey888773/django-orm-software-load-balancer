from .abstractions import ReadRepositoryInterface, WriteRepositoryInterface, LoadBalancingStrategyInterface
from .lb_strategy import RoundRobinStrategy
from ..database import DatabaseWrapper
from ..events import *
from ..models.todo_item import TodoItem
from schemas import TodoItemSchema, Response
import asyncio


class LoadBalancerReadRepository(ReadRepositoryInterface):
    def __init__(self, dbws: list[DatabaseWrapper], default_strategy: LoadBalancingStrategyInterface=RoundRobinStrategy()):
        self.db_wrappers = {dbw.get_id(): dbw for dbw in dbws}
        self.strategy = default_strategy

    async def list_todo_items(self) -> list[TodoItem]:
        dbw = await self.strategy.choose(list(self.db_wrappers.values()))
        await dbw.commit_events()
        with dbw.make_session() as db:
            return db.query(TodoItem).all()

    async def get_todo_item_by_id(self, id: int) -> TodoItem:
        dbw = await self.strategy.choose(list(self.db_wrappers.values()))
        await dbw.commit_events()
        with dbw.make_session() as db:
            return db.query(TodoItem).filter(TodoItem.id == id).first()


class LoadBalancerWriteRepository(WriteRepositoryInterface):
    def __init__(self, dbws: list[DatabaseWrapper]):
        self.db_wrappers = {dbw.get_id(): dbw for dbw in dbws}

    async def create_todo_item(self, todo_item: TodoItemSchema) -> TodoItem:
        event = TodoItemCreatedEvent(title=todo_item.title, description=todo_item.description, completed=todo_item.completed)
        await self._process_event(event)

    async def update_todo_item(self, id: int, todo_item: TodoItemSchema) -> TodoItem:
        event = TodoItemUpdatedEvent(id=id, title=todo_item.title, description=todo_item.description, completed=todo_item.completed)
        await self._process_event(event)

    async def delete_todo_item(self, id: int) -> Response:
        event = TodoItemDeletedEvent(id=id)
        await self._process_event(event)

    async def _process_event(self, event: EventInterface):
        async def commit_events(dbw: DatabaseWrapper):
            if await dbw.is_connected():
                await dbw.commit_events()

        tasks = []
        for _, dbw in self.db_wrappers.items():
            dbw.register_event(event)
            tasks.append(commit_events(dbw))

        await asyncio.gather(*tasks)