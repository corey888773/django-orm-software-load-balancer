from commands import *
from querries import *
from .. import todo_item_repository

commands_mediator = CommandsMediator()
commands_mediator.register(CreateTodoItemCommand, CreateTodoItemCommandHandler(repository=todo_item_repository, unitOfWork=unitOfWork))
commands_mediator.register(UpdateTodoItemCommand, UpdateTodoItemCommandHandler(repository=todo_item_repository, unitOfWork=unitOfWork))
commands_mediator.register(DeleteTodoItemCommand, DeleteTodoItemCommandHandler(repository=todo_item_repository, unitOfWork=unitOfWork))

querries_mediator = QuerriesMediator()
querries_mediator.register(ListTodoItemsQuerry, ListTodoItemsQuerryHandler(repository=todo_item_repository))
querries_mediator.register(GetTodoItemByIdQuerry, GetTodoItemByIdQuerryHandler(repository=todo_item_repository))