from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
from data import db_load_balancer, todo_repository

router = APIRouter()

@router.post('/')
async def create_todo_item(request: RequestTodoItem):
    for r in todo_repository:
        r.create_todo_item(todo_item=request)
    return Response(code="200", status="OK", message="Todo Item Created", result=None).dict(exclude_none=True)

@router.get('/')
async def list_todo_items():
    for r in todo_repository:
        _books = r.list_todo_items()
    return Response(code="200", status="OK", message="Todo Items Retrieved", result=_books).dict(exclude_none=True)

@router.get('/{id}')
async def get_todo_item_by_id(id: int):
    for r in todo_repository:
        _book = r.get_todo_item_by_id(id=id)
    return Response(code="200", status="OK", message="Todo Item Retrieved", result=_book).dict(exclude_none=True)

@router.delete('/{id}')
async def delete_todo_item(id: int):
    for r in todo_repository:
        r.delete_todo_item(id=id)
    return Response(code="200", status="OK", message="Todo Item Deleted", result=None).dict(exclude_none=True)

@router.put('/{id}')
async def update_todo_item(id: int, request: RequestTodoItem):
    for r in todo_repository:
        r.update_todo_item(id=id, todo_item=request)
    return Response(code="200", status="OK", message="Todo Item Updated", result=None).dict(exclude_none=True)

