import abc
from sqlalchemy.orm import Session
from .abstractions import UnitOfWorkInterface

class UnitOfWork(UnitOfWorkInterface):
    def __init__(self, session):
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def refresh(self, obj):
        self.session.refresh(obj)