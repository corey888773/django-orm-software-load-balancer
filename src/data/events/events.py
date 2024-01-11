import abc
from dataclasses import dataclass
from .abstractions import EventInterface, EventHandlerInterface, UnitOfWorkInterface, WriteRepositoryInterface, ReadRepositoryInterface
from ..models.todo_item import TodoItem


@dataclass
class TodoItemCreatedEvent(EventInterface):
    title: str
    description: str
    completed: bool


@dataclass
class TodoItemUpdatedEvent(EventInterface):
    id: int
    title: str
    description: str
    completed: bool


@dataclass
class TodoItemDeletedEvent(EventInterface):
    id: int

@dataclass
class GetTodoItemByIdEvent(EventInterface):
    id: int

@dataclass
class ListTodoItemsEvent(EventInterface):
    pass

class TodoItemCreatedEventHandler(EventHandlerInterface):
    def __init__(self, repository: any, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    async def handle(self, event : TodoItemCreatedEvent):
        _todo_item = TodoItem(title=event.title, description=event.description, completed=event.completed)
        todo_item = await self.repository.create_todo_item(_todo_item)
        # self.unitOfWork.commit()
        return _todo_item


class TodoItemUpdatedEventHandler(EventHandlerInterface):
    def __init__(self, repository: any, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    async def handle(self, event : TodoItemUpdatedEvent):
        _todo_item = self.repository.get_todo_item_by_id(event.id)
        _todo_item.title = event.title
        _todo_item.description = event.description
        _todo_item.completed = event.completed
        await self.repository.update_todo_item(_todo_item)
        # self.unitOfWork.commit()
        return _todo_item


class TodoItemDeletedEventHandler(EventHandlerInterface):
    def __init__(self, repository: any, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    async def handle(self, event : TodoItemDeletedEvent):
        _todo_item = self.repository.get_todo_item_by_id(event.id)
        await self.repository.delete_todo_item(_todo_item)
        # self.unitOfWork.commit()
        return _todo_item


class GetTodoItemByIdEventHandler(EventHandlerInterface):
    def __init__(self, repository: any, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    async def handle(self, event : GetTodoItemByIdEvent):
        _todo_item = await self.repository.get_todo_item_by_id(event.id)
        return _todo_item


class ListTodoItemsEventHandler(EventHandlerInterface):
    def __init__(self, repository: any, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    async def handle(self, event : ListTodoItemsEvent):
        _todo_items = await self.repository.list_todo_items()
        return _todo_items


# design pattern: mediator
class EventsMediator:
    def __init__(self):
        self.event_handlers : Dict[EventInterface, EventHandlerInterface] = {}

    def register(self, event: EventInterface, event_handler: EventHandlerInterface):
        self.event_handlers[event] = event_handler

    async def handle(self, event: EventInterface):
        return await self.event_handlers[event.__class__].handle(event)