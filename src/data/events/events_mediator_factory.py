from ..abstractions import TodoItemRepositoryInterface, UnitOfWorkInterface
from .events import *

class EventsMediatorFactory:
    def create(repository : TodoItemRepositoryInterface, unit_of_work: UnitOfWorkInterface) -> EventsMediator:
        events_mediator = EventsMediator()
        events_mediator.register(TodoItemCreatedEvent, TodoItemCreatedEventHandler(repository=repository, unitOfWork=unit_of_work))
        events_mediator.register(TodoItemUpdatedEvent, TodoItemUpdatedEventHandler(repository=repository, unitOfWork=unit_of_work))
        events_mediator.register(TodoItemDeletedEvent, TodoItemDeletedEventHandler(repository=repository, unitOfWork=unit_of_work))
        events_mediator.register(GetTodoItemByIdEvent, GetTodoItemByIdEventHandler(repository=repository, unitOfWork=unit_of_work))
        events_mediator.register(ListTodoItemsEvent, ListTodoItemsEventHandler(repository=repository, unitOfWork=unit_of_work))

        return events_mediator
    