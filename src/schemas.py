from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class TodoItemSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = False

    class Config:
        orm_mode = True


class RequestTodoItem(BaseModel):
    parameter: TodoItemSchema = Field(..., example={
        "title": "string",
        "description": "string",
        "completed": True
    })


class Response(GenericModel, Generic[T]):
    def __init__(self, code: int, status: str, message: Optional[str] = None, result: Optional[T] = None):
        code: str
        status: str
        message: str
        result: Optional[T]
