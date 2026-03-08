from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel,Session, select
from db import engine
from auth import create_token
from models import User,UserCreate, UserRead, UserLogin
app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello world"}

@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)

def create_session():
    with Session(engine) as session:
        yield session

@app.post("/signup",response_model=UserRead)
async def signup(user : UserCreate,db:Session =  Depends(create_session)):
    email = user.email.lower().strip()

    statement = select(User).where(User.email==email)
    existing_user = db.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User Already exists");
    db_user = User(
        name = user.name,
        email = email,
        password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return (db_user)

@app.post("/login")
async def login(user: UserLogin, db : Session = Depends(create_session)):

    email = user.email.lower().strip()

    statement = select(User).where(User.email==email)
    db_user = db.exec(statement).first()

    if not db_user or user.password!= db_user.password:
        raise HTTPException(status_code=400, detail="Invalid Credentials," \
        "either Email or Password")


    access_token = create_token(db_user.id,db_user.name)
    
    return {
        "access_token ": access_token
    }


