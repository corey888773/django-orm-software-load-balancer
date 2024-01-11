import abc
from ..repository.abstractions import ReadRepositoryInterface, WriteRepositoryInterface, UnitOfWorkInterface

class EventInterface(metaclass=abc.ABCMeta):
    pass

class EventHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def handle(self, event: EventInterface):
        raise NotImplementedError