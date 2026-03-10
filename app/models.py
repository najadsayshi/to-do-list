from datetime import datetime
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel

class User(SQLModel, table = True):
    id : int | None = Field(default=None,primary_key=True)
    name : str
    email : str = Field(index= True, unique=True)
    password : str
    

class UserCreate(SQLModel):
    name : str
    email : str
    password : str
    

class UserRead(SQLModel):
    name : str
    email : str


class UserLogin(SQLModel):
    email : str
    password : str

#model for jwt token
class Token(BaseModel):
    access_token : str
    token_type : str


class Priority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Todo(SQLModel, table = True):
    id : Optional[int] =  Field(default=None,primary_key=True)
    description : str
    completed : bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    due_date : Optional[datetime] = None
    priority : Priority = Field(default=Priority.medium)
    owner_id : int = Field(foreign_key="user.id")


class TodoCreate(SQLModel):
    description : str
    due_date : Optional[datetime] = None
    priority : Priority = Priority.low  


class TodoRead(SQLModel):
    id : int
    description : str
    completed : bool
    created_at : datetime
    due_date : Optional[datetime]
    priority : Priority


class TodoUpdate(SQLModel):
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
