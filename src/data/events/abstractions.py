import abc

class EventInterface(metaclass=abc.ABCMeta):
    pass

class EventHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, event: EventInterface):
        raise NotImplementedError