from typing import Type, Dict
import abc
from dataclasses import dataclass
from .abstractions import CommandInterface, CommandHandlerInterface
from ..abstractions import TodoItemRepositoryInterface, UnitOfWorkInterface
from ..models.todo_item import TodoItem

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

class DeleteTodoItemCommand(CommandInterface):
    id: int

class CreateTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    def handle(self, command : CreateTodoItemCommand):
        _todo_item = TodoItem(title=command.title, description=command.description, completed=command.completed)
        self.repository.create_todo_item(_todo_item)
        self.unitOfWork.commit()
        return _todo_item

class UpdateTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    def handle(self, command : UpdateTodoItemCommand):
        _todo_item = self.repository.get_todo_item_by_id(command.id)
        _todo_item.title = command.title
        _todo_item.description = command.description
        _todo_item.completed = command.completed
        self.repository.update_todo_item(_todo_item)
        self.unitOfWork.commit()
        return _todo_item

class DeleteTodoItemCommandHandler(CommandHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface, unitOfWork: UnitOfWorkInterface):
        self.repository = repository
        self.unitOfWork = unitOfWork

    def handle(self, command : DeleteTodoItemCommand):
        self.repository.delete_todo_item(command.id)
        self.unitOfWork.commit()
        return Response(code="200", status="OK", message="Todo Item Deleted", result=None)


# design pattern: mediator
class CommandsMediator:
    def __init__(self):
        self.handlers: Dict[CommandInterface, CommandHandlerInterface] = {}

    def register(self, command: CommandInterface, handler: CommandHandlerInterface):
        self.handlers[command] = handler

    def execute(self, command: CommandInterface):
        return self.handlers[command].handle(command)

