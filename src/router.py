from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
import todo_crud
from dbloadbalancer import dbLoadBalancer

router = APIRouter()

@router.post('/')
async def create_todo_item(request: RequestTodoItem, db: Session = Depends(dbLoadBalancer.get_sessions)):
    todo_repository = todo_crud.TodoItemRepository(db=db)
    todo_repository.create_todo_item(todo_item=request)
    return Response(code="200", status="OK", message="Todo Item Created", result=None).dict(exclude_none=True)

@router.get('/')
async def list_todo_items(db: Session = Depends(dbLoadBalancer.get_sessions)):
    todo_repository = todo_crud.TodoItemRepository(db=db)
    _books = todo_repository.list_todo_items()
    return Response(code="200", status="OK", message="Todo Items Retrieved", result=_books).dict(exclude_none=True)

@router.get('/{id}')
async def get_todo_item_by_id(id: int, db: Session = Depends(dbLoadBalancer.get_sessions)):
    todo_repository = todo_crud.TodoItemRepository(db=db)
    _book = todo_repository.get_todo_item_by_id(id=id)
    return Response(code="200", status="OK", message="Todo Item Retrieved", result=_book).dict(exclude_none=True)

@router.delete('/{id}')
async def delete_todo_item(id: int, db: Session = Depends(dbLoadBalancer.get_sessions)):
    todo_repository = todo_crud.TodoItemRepository(db=db)
    return todo_repository.delete_todo_item(id=id)

@router.put('/{id}')
async def update_todo_item(id: int, request: RequestTodoItem, db: Session = Depends(dbLoadBalancer.get_sessions)):
    todo_repository = todo_crud.TodoItemRepository(db=db)
    todo_repository.update_todo_item(id=id, todo_item=todo_item)
    return Response(code="200", status="OK", message="Todo Item Updated", result=None).dict(exclude_none=True)

