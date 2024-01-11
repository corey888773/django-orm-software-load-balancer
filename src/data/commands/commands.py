from typing import Type, Dict, List
import abc
from dataclasses import dataclass
from .abstractions import CommandInterface, CommandHandlerInterface, WriteRepositoryInterface, UnitOfWorkInterface
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
    def __init__(self, repository: WriteRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        # self.unitOfWork = unitOfWork

    async def handle(self, command : CreateTodoItemCommand):
        _todo_item = TodoItemSchema(title=command.title, description=command.description, completed=command.completed)
        await self.repository.create_todo_item(_todo_item)
        return _todo_item


class UpdateTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repository: WriteRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        # self.unitOfWork = unitOfWork

    async def handle(self, command : UpdateTodoItemCommand):
        _todo_item = TodoItemSchema(id=command.id, title=command.title, description=command.description, completed=command.completed)
        await self.repository.update_todo_item(id=command.id, todo_item=_todo_item)
        return _todo_item


class DeleteTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repository: WriteRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        # self.unitOfWork = unitOfWork

    async def handle(self, command : DeleteTodoItemCommand):
        await self.repository.delete_todo_item(command.id)
        return ""


# design pattern: mediator
class CommandsMediator:
    def __init__(self):
        self.handlers: Dict[CommandInterface, CommandHandlerInterface] = {}

    def register(self, command: CommandInterface, handler: CommandHandlerInterface):
        self.handlers[command] = handler

    async def execute(self, command: CommandInterface):
        return await self.handlers[command.__class__].handle(command)

