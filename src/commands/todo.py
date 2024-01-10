
from typing import Type, Dict
import abc

class CommandInterface(metaclass=abc.ABCMeta):
    pass


class CreateTodoItemCommand(CommandInterface):
    def __init__(self, title: str, description: str, completed: bool):
        self.title = title
        self.description = description
        self.completed = completed

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_completed(self):
        return self.completed


class CommandHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, command: CommandInterface):
        pass


class CreateTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    def handle(self, command : CommandInterface):
        pass


class Mediator:
    def __init__(self):
        self.handlers: Dict[CommandInterface, CommandHandlerInterface] = {}

    def register(self, command: CommandInterface, handler: CommandHandlerInterface):
        self.handlers[command] = handler

    def execute(self, command: CommandInterface):
        return self.handlers[command].handle(command)

    