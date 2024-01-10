class CommandInterface(metaclass=abc.ABCMeta):
    raise NotImplementedError


class CommandHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, command: CommandInterface):
        raise NotImplementedError


class QuerryInterface(metaclass=abc.ABCMeta):
    pass

class QuerryHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, querry: QuerryInterface):
        raise NotImplementedError
