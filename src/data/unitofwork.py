import abc

class UnitOfWorkInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self):
        raise NotImplementedError

class UnitOfWork(UnitOfWorkInterface):
    def __init__(self, session):
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def refresh(self, obj):
        self.session.refresh(obj)