from .abstractions import UnitOfWorkInterface, ReadRepositoryInterface, WriteRepositoryInterface
from .events import *

# design pattern: factory
class EventsDispatcherFactory:
    def create(rrepo: ReadRepositoryInterface, wrepo: WriteRepositoryInterface, unit_of_work: UnitOfWorkInterface) -> EventsDispatcher:
        events_dispatcher = EventsDispatcher()
        events_dispatcher.register(TodoItemCreatedEvent, TodoItemCreatedEventHandler(repository=wrepo, unitOfWork=unit_of_work))
        events_dispatcher.register(TodoItemUpdatedEvent, TodoItemUpdatedEventHandler(wrepository=wrepo, rrepository=rrepo, unitOfWork=unit_of_work))
        events_dispatcher.register(TodoItemDeletedEvent, TodoItemDeletedEventHandler(wrepository=wrepo, rrepository=rrepo, unitOfWork=unit_of_work))

        return events_dispatcher
    