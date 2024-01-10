from typing import Type, Dict, List
import abc
from dataclasses import dataclass
from .abstractions import CommandInterface, CommandHandlerInterface
from ..abstractions import TodoItemRepositoryInterface, UnitOfWorkInterface
from schemas import TodoItemSchema

@dataclass
class CreateTodoItemCommand(CommandInterface):
    title: str
    description: str
    completed: bool

@dataclass
class UpdateTodoItemCommand(CommandInterface):
    id: int
    title: str
    description: str
    completed: bool

@dataclass
class DeleteTodoItemCommand(CommandInterface):
    id: int

class CreateTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repositories: List[TodoItemRepositoryInterface], unitOfWork: UnitOfWorkInterface):
        self.repositories = repositories
        # self.unitOfWork = unitOfWork

    def handle(self, command : CreateTodoItemCommand):
        _todo_item = TodoItemSchema(title=command.title, description=command.description, completed=command.completed)
        for r in self.repositories:
            try:
                r.create_todo_item(_todo_item)
                print('command handler: create todo item')
            except Exception as e:
                print(e)
        return _todo_item

class UpdateTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repositories: List[TodoItemRepositoryInterface], unitOfWork: UnitOfWorkInterface):
        self.repositories = repositories
        # self.unitOfWork = unitOfWork

    def handle(self, command : UpdateTodoItemCommand):
        _todo_item = TodoItemSchema(id=command.id, title=command.title, description=command.description, completed=command.completed)
        for r in self.repositories:
            r.update_todo_item(id=command.id, todo_item=_todo_item)
        return _todo_item

class DeleteTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repositories: List[TodoItemRepositoryInterface], unitOfWork: UnitOfWorkInterface):
        self.repositories = repositories
        # self.unitOfWork = unitOfWork

    def handle(self, command : DeleteTodoItemCommand):
        for r in self.repositories:
            r.delete_todo_item(command.id)
        return ""


# design pattern: mediator
class CommandsMediator:
    def __init__(self):
        self.handlers: Dict[CommandInterface, CommandHandlerInterface] = {}

    def register(self, command: CommandInterface, handler: CommandHandlerInterface):
        self.handlers[command] = handler

    def execute(self, command: CommandInterface):
        return self.handlers[command.__class__].handle(command)

