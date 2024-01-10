from .commands import *
from .queries import *
from .. import todo_repository, unit_of_work

commands_mediator = CommandsMediator()
commands_mediator.register(CreateTodoItemCommand, CreateTodoItemCommandHandler(repositories=todo_repository, unitOfWork=unit_of_work))
commands_mediator.register(UpdateTodoItemCommand, UpdateTodoItemCommandHandler(repositories=todo_repository, unitOfWork=unit_of_work))
commands_mediator.register(DeleteTodoItemCommand, DeleteTodoItemCommandHandler(repositories=todo_repository, unitOfWork=unit_of_work))

queries_mediator = QueriesMediator()
queries_mediator.register(ListTodoItemsQuery, ListTodoItemsQueryHandler(repositories=todo_repository))
queries_mediator.register(GetTodoItemByIdQuery, GetTodoItemByIdQueryHandler(repositories=todo_repository))