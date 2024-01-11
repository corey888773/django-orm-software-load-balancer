from .commands import *
from .queries import *
from .. import todo_repositories, unit_of_work, events_repositories

commands_mediator = CommandsMediator()
commands_mediator.register(CreateTodoItemCommand, CreateTodoItemCommandHandler(repositories=todo_repositories, unitOfWork=unit_of_work))
commands_mediator.register(UpdateTodoItemCommand, UpdateTodoItemCommandHandler(repositories=todo_repositories, unitOfWork=unit_of_work))
commands_mediator.register(DeleteTodoItemCommand, DeleteTodoItemCommandHandler(repositories=todo_repositories, unitOfWork=unit_of_work))

queries_mediator = QueriesMediator()
queries_mediator.register(ListTodoItemsQuery, ListTodoItemsQueryHandler(repositories=todo_repositories))
queries_mediator.register(GetTodoItemByIdQuery, GetTodoItemByIdQueryHandler(repositories=todo_repositories))