import abc
from dataclasses import dataclass
from .abstractions import TodoItemRepositoryInterface, UnitOfWorkInterface, EventInterface, EventHandlerInterface


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


class TodoItemCreatedEventHandler(EventHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    def handle(self, event : TodoItemCreatedEvent):
        _todo_item = TodoItem(title=event.title, description=event.description, completed=event.completed)
        self.repository.create_todo_item(_todo_item)
        self.unitOfWork.commit()
        return _todo_item


class TodoItemUpdatedEventHandler(EventHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    def handle(self, event : TodoItemUpdatedEvent):
        _todo_item = self.repository.get_todo_item_by_id(event.id)
        _todo_item.title = event.title
        _todo_item.description = event.description
        _todo_item.completed = event.completed
        self.repository.update_todo_item(_todo_item)
        self.unitOfWork.commit()
        return _todo_item


class TodoItemDeletedEventHandler(EventHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    def handle(self, event : TodoItemDeletedEvent):
        _todo_item = self.repository.get_todo_item_by_id(event.id)
        self.repository.delete_todo_item(_todo_item)
        self.unitOfWork.commit()
        return _todo_item


# design pattern: mediator
class EventsMediator:
    def __init__(self):
        self.event_handlers : Dict[EventInterface, EventHandlerInterface] = {}

    def register(self, event: EventInterface, event_handler: EventHandlerInterface):
        self.event_handlers[event] = event_handler

    def handle(self, event: EventInterface):
        event_name = type(event).__name__
        return self.event_handlers[event_name].handle(event)