from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel

class User(SQLModel, table = True):
    id : int | None = Field(default=None,primary_key=True)
    name : str
    email : str
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


