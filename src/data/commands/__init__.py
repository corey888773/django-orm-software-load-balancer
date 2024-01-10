from commands import *
from querries import *

commands_mediator = CommandsMediator()
commands_mediator.register(CreateTodoItemCommand, CreateTodoItemCommandHandler(repository=todoItemRepository, unitOfWork=unitOfWork))
commands_mediator.register(UpdateTodoItemCommand, UpdateTodoItemCommandHandler(repository=todoItemRepository, unitOfWork=unitOfWork))
commands_mediator.register(DeleteTodoItemCommand, DeleteTodoItemCommandHandler(repository=todoItemRepository, unitOfWork=unitOfWork))

querries_mediator = QuerriesMediator()
querries_mediator.register(ListTodoItemsQuerry, ListTodoItemsQuerryHandler(repository=todo_item_repository))
querries_mediator.register(GetTodoItemByIdQuerry, GetTodoItemByIdQuerryHandler(repository=todo_item_repository))