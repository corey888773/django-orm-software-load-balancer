from .config import DATABASE_URLS
from . import models
from .repository import *
from .database import DatabaseWrapper
from .unitofwork import UnitOfWork
from .events import *
from .commands import *

dbs = []
for idx, url in enumerate(DATABASE_URLS):
    database = DatabaseWrapper(conn_str=url, id=f'database{idx+1}')
    database.migrate(models.todo_item)

    default_read_repository = DefaultReadRepository(dbw=database)
    default_write_repository = DefaultWriteRepository(dbw=database)

    database.events_mediator = EventsMediatorFactory.create(rrepo=default_read_repository, wrepo=default_write_repository, unit_of_work=UnitOfWork(database))
    dbs.append(database)

event_read_repositories = [EventsReadRepository(dbw=dbw) for dbw in dbs]
event_write_repositories = [EventsWriteRepository(dbw=dbw) for dbw in dbs]

lb_read_repository = LoadBalancerReadRepository(dbws=dbs)
lb_write_repository = LoadBalancerWriteRepository(dbws=dbs)

unit_of_work = UnitOfWork(None)


commands_mediator = CommandsMediator()
commands_mediator.register(CreateTodoItemCommand, CreateTodoItemCommandHandler(repository=lb_write_repository, unitOfWork=unit_of_work))
commands_mediator.register(UpdateTodoItemCommand, UpdateTodoItemCommandHandler(repository=lb_write_repository, unitOfWork=unit_of_work))
commands_mediator.register(DeleteTodoItemCommand, DeleteTodoItemCommandHandler(repository=lb_write_repository, unitOfWork=unit_of_work))

queries_mediator = QueriesMediator()
queries_mediator.register(ListTodoItemsQuery, ListTodoItemsQueryHandler(repository=lb_read_repository))
queries_mediator.register(GetTodoItemByIdQuery, GetTodoItemByIdQueryHandler(repository=lb_read_repository))