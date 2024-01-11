from .config import DATABASE_URLS
from . import models
from .repository import *
from .database import DatabaseWrapper
from .events import *
from .commands import *

dbs = []
for idx, url in enumerate(DATABASE_URLS):
    database = DatabaseWrapper(conn_str=url, id=f'database{idx+1}')
    database.migrate(models.todo_item)

    default_read_repository = DefaultReadRepository(dbw=database)
    default_write_repository = DefaultWriteRepository(dbw=database)

    database.events_dispatcher = EventsDispatcherFactory.create(rrepo=default_read_repository, wrepo=default_write_repository, unit_of_work=NoneUnitOfWork())
    dbs.append(database)

lb_read_repository = LoadBalancerReadRepository(dbws=dbs)
lb_write_repository = LoadBalancerWriteRepository(dbws=dbs)

unit_of_work = NoneUnitOfWork()

commands_invoker = CommandsInvoker()
commands_invoker.register(CreateTodoItemCommand, CreateTodoItemCommandHandler(repository=lb_write_repository, unitOfWork=unit_of_work))
commands_invoker.register(UpdateTodoItemCommand, UpdateTodoItemCommandHandler(repository=lb_write_repository, unitOfWork=unit_of_work))
commands_invoker.register(DeleteTodoItemCommand, DeleteTodoItemCommandHandler(repository=lb_write_repository, unitOfWork=unit_of_work))

queries_invoker = QueriesInvoker()
queries_invoker.register(ListTodoItemsQuery, ListTodoItemsQueryHandler(repository=lb_read_repository))
queries_invoker.register(GetTodoItemByIdQuery, GetTodoItemByIdQueryHandler(repository=lb_read_repository))