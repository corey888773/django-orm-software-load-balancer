from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URLS =[
    "postgresql://postgres:postgres@db1:5432/todo",
    # "postgresql://postgres:postgres@db2:5432/todo"
]


Base = declarative_base()

