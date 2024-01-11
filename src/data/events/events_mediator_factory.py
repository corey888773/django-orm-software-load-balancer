from .abstractions import UnitOfWorkInterface, ReadRepositoryInterface, WriteRepositoryInterface
from .events import *

class EventsMediatorFactory:
    def create(rrepo: ReadRepositoryInterface, wrepo: WriteRepositoryInterface, unit_of_work: UnitOfWorkInterface) -> EventsMediator:
        events_mediator = EventsMediator()
        events_mediator.register(TodoItemCreatedEvent, TodoItemCreatedEventHandler(repository=wrepo, unitOfWork=unit_of_work))
        events_mediator.register(TodoItemUpdatedEvent, TodoItemUpdatedEventHandler(repository=wrepo, unitOfWork=unit_of_work))
        events_mediator.register(TodoItemDeletedEvent, TodoItemDeletedEventHandler(repository=wrepo, unitOfWork=unit_of_work))
        events_mediator.register(GetTodoItemByIdEvent, GetTodoItemByIdEventHandler(repository=rrepo, unitOfWork=unit_of_work))
        events_mediator.register(ListTodoItemsEvent, ListTodoItemsEventHandler(repository=rrepo, unitOfWork=unit_of_work))

        return events_mediator
    