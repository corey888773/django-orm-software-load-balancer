from sqlalchemy import Column, Integer, String, Boolean
from ..config import Base

class TodoItem(Base):
    __tablename__ = "todo_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)