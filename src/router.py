from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
import todo_crud
from dbloadbalancer import *

router = APIRouter()

def get_db():
    sessions = dbLoadBalancer.get_sessions()
    try:
        for session in sessions:
            yield session()
    finally:
        dbLoadBalancer.close_sessions(sessions)

@router.post('/')
async def create_todo_item(request: RequestTodoItem, db: Session = Depends(get_db)):
    print(type(Session))
    todo_crud.create_todo_item(db=db, todo_item=request)
    return Response(code="200", status="OK", message="Todo Item Created", result=None).dict(exclude_none=True)

@router.get('/')
async def list_todo_items(db: Session = Depends(get_db)):
    _books = todo_crud.list_todo_items(db=db)
    return Response(code="200", status="OK", message="Todo Items Retrieved", result=_books).dict(exclude_none=True)

@router.get('/{id}')
async def get_todo_item_by_id(id: int, db: Session = Depends(get_db)):
    _book = todo_crud.get_todo_item_by_id(db=db, id=id)
    return Response(code="200", status="OK", message="Todo Item Retrieved", result=_book).dict(exclude_none=True)

@router.delete('/{id}')
async def delete_todo_item(id: int, db: Session = Depends(get_db)):
    return todo_crud.delete_todo_item(db=db, id=id)

@router.put('/{id}')
async def update_todo_item(id: int, request: RequestTodoItem, db: Session = Depends(get_db)):
    todo_crud.update_todo_item(db=db, id=id, todo_item=todo_item)
    return Response(code="200", status="OK", message="Todo Item Updated", result=None).dict(exclude_none=True)

