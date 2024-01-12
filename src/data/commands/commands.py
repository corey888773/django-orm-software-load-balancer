from typing import Type, Dict, List
import abc
from dataclasses import dataclass
from .abstractions import CommandInterface, CommandHandlerInterface, WriteRepositoryInterface, UnitOfWorkInterface
from schemas import TodoItemSchema

# https://sbcode.net/python/command/
# command pattern

@dataclass
class CreateTodoItemCommand(CommandInterface):
    # works as a data class and implements empty CommandInterface
    title: str
    description: str
    completed: bool


@dataclass
class UpdateTodoItemCommand(CommandInterface):
    # works as a data class and implements empty CommandInterface
    id: int
    title: str
    description: str
    completed: bool


@dataclass
class DeleteTodoItemCommand(CommandInterface):
    # works as a data class and implements empty CommandInterface
    id: int


class CreateTodoItemCommandHandler(CommandHandlerInterface):
    # works as a command class in the command pattern. It implements command handler interface which has handle method
    def __init__(self, repository: WriteRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        # repository in this case is the receiver in the command pattern
        self.repository = repository
        self.unitOfWork = unitOfWork # Not implemented

    async def handle(self, command : CommandInterface):
        _todo_item = TodoItemSchema(title=command.title, description=command.description, completed=command.completed)
        await self.repository.create_todo_item(_todo_item)
        return _todo_item


class UpdateTodoItemCommandHandler(CommandHandlerInterface):
    # works as a command class in the command pattern. It implements command handler interface which has handle method  
    def __init__(self, repository: WriteRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        # repository in this case is the receiver in the command pattern
        self.repository = repository
        self.unitOfWork = unitOfWork # Not implemented

    async def handle(self, command : CommandInterface):
        _todo_item = TodoItemSchema(id=command.id, title=command.title, description=command.description, completed=command.completed)
        await self.repository.update_todo_item(id=command.id, todo_item=_todo_item)
        return _todo_item


class DeleteTodoItemCommandHandler(CommandHandlerInterface):
    # works as a command class in the command pattern. It implements command handler interface which has handle method
    def __init__(self, repository: WriteRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        # repository in this case is the receiver in the command pattern
        self.repository = repository
        self.unitOfWork = unitOfWork # Not implemented

    async def handle(self, command : CommandInterface):
        await self.repository.delete_todo_item(command.id)
        return ""


class CommandsInvoker:
    # works as a invoker class in the command pattern. It has register method and execute method which executes the commandhandler's handle method
    def __init__(self):
        self.handlers: Dict[CommandInterface, CommandHandlerInterface] = {}

    def register(self, command: CommandInterface, handler: CommandHandlerInterface):
        self.handlers[command] = handler

    async def execute(self, command: CommandInterface):
        return await self.handlers[command.__class__].handle(command)

