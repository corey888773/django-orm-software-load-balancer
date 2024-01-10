import abc

class QuerryInterface(metaclass=abc.ABCMeta):
    pass

class ListTodoItemsQuerry(QuerryInterface):
    pass

class GetTodoItemByIdQuerry(QuerryInterface):
    id: int

class QuerryHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, querry: QuerryInterface):
        pass

class ListTodoItemsQuerryHandler(QuerryHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface):
        self.repository = repository

    def handle(self, querry: QuerryInterface):
        return self.repository.list_todo_items()

class GetTodoItemByIdQuerryHandler(QuerryHandlerInterface):
    def __init__(self, repository: TodoItemRepositoryInterface):
        self.repository = repository

    def handle(self, querry: QuerryInterface):
        return self.repository.get_todo_item_by_id(querry.id)


# design pattern: mediator
class QuerriesMediator:
    def __init__(self):
        self.querry_handlers : Dict[QuerryInterface, QuerryHandlerInterface] = {}

    def register(self, querry: QuerryInterface, querry_handler: QuerryHandlerInterface):
        self.querry_handlers[querry] = querry_handler

    def handle(self, querry: QuerryInterface):
        querry_name = type(querry).__name__
        return self.querry_handlers[querry_name].handle(querry)


querries_mediator = QuerriesMediator()
querries_mediator.register(ListTodoItemsQuerry, ListTodoItemsQuerryHandler(repository=todo_item_repository))
querries_mediator.register(GetTodoItemByIdQuerry, GetTodoItemByIdQuerryHandler(repository=todo_item_repository))