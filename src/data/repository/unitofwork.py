import abc
from sqlalchemy.orm import Session
from .abstractions import UnitOfWorkInterface

class NoneUnitOfWork(UnitOfWorkInterface):
    def __init__(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def refresh(self, obj):
        pass
