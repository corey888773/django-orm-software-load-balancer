import abc
from ..abstractions import UnitOfWorkInterface
from ..repository.abstractions import ReadRepositoryInterface, WriteRepositoryInterface

class EventInterface(metaclass=abc.ABCMeta):
    pass

class EventHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def handle(self, event: EventInterface):
        raise NotImplementedError