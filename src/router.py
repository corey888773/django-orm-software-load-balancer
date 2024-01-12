from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from schemas import TodoItemSchema, RequestTodoItem, Response
from data import *

router = APIRouter()


@router.post('/')
async def create_todo_item(request: RequestTodoItem):
    create_todo_item_command = CreateTodoItemCommand(title=request.parameter.title, description=request.parameter.description, completed=request.parameter.completed)
    try:
        await commands_invoker.execute(create_todo_item_command)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Response(code="200", status="OK", message="Todo Item Created", result=None).dict(exclude_none=True)


@router.get('/')
async def list_todo_items():
    list_todo_items_query = ListTodoItemsQuery()
    try:
        _books = await queries_invoker.execute(list_todo_items_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if _books is None or len(_books) == 0:
        raise HTTPException(status_code=404, detail="Todo Items Not Found")

    return Response(code="200", status="OK", message="Todo Items Retrieved", result=_books).dict(exclude_none=True)


@router.get('/{id}')
async def get_todo_item_by_id(id: int):
    get_todo_item_by_id_query = GetTodoItemByIdQuery(id=id)
    try:
        _book = await queries_invoker.execute(get_todo_item_by_id_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if _book is None:
        raise HTTPException(status_code=404, detail="Todo Item Not Found")

    return Response(code="200", status="OK", message="Todo Item Retrieved", result=_book).dict(exclude_none=True)


@router.delete('/{id}')
async def delete_todo_item(id: int):
    delete_todo_item_command = DeleteTodoItemCommand(id=id)
    try:
        await commands_invoker.execute(delete_todo_item_command)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Response(code="200", status="OK", message="Todo Item Deleted", result=None).dict(exclude_none=True)


@router.put('/{id}')
async def update_todo_item(id: int, request: RequestTodoItem):
    update_todo_item_command = UpdateTodoItemCommand(id=id, title=request.parameter.title, description=request.parameter.description, completed=request.parameter.completed)
    try:
        await commands_invoker.execute(update_todo_item_command)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return Response(code="200", status="OK", message="Todo Item Updated", result=None).dict(exclude_none=True)

