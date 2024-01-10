from fastapi import FastAPI
from config import DATABASE_URLS
from dbloadbalancer import DbLoadBalancer
import router
import models.todo_item

dbLoadBalancer = DbLoadBalancer(DATABASE_URLS)
dbLoadBalancer.migrate(models.todo_item)

app = FastAPI()

app.include_router(router.router, prefix="/todo", tags=["todo"])