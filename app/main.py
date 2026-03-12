from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import  HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import SQLModel,Session, select
from db import engine
from auth import create_token, verify_token
from models import User,UserCreate, UserRead, UserLogin, Todo,TodoCreate,TodoRead, TodoUpdate
#imports for pagination
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlmodel import paginate
app = FastAPI()
add_pagination(app)
@app.get("/")
async def root():
    return {"message":"Hello world"}

#cors for frontend to access the api from different origin
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)

def create_session():
    with Session(engine) as session:
        yield session

@app.post("/signup",response_model=UserRead, status_code=201)
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
        "access_token": access_token
    }


security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                    db : Session = Depends(create_session)
                    ):
    token = credentials.credentials

    try:
        payload = verify_token(token)

        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload["sub"]

        statement = select(User).where(User.id == user_id)

        user = db.exec(statement).first()
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")    



#paginated api
@app.get("/todos", response_model=Page[TodoRead])
async def get_todos(
    db: Session = Depends(create_session),
    current_user: User = Depends(get_current_user),
) -> Page[TodoRead]:

    statement = (
        select(Todo)
        .where(Todo.owner_id == current_user.id)
        .order_by(Todo.created_at.desc())
    )

    return paginate(db, statement)

@app.post("/todos", response_model=TodoRead, status_code =201)
async def create_todo(
    todo : TodoCreate,
    db : Session = Depends(create_session),
    current_user: User = Depends(get_current_user)
):
    db_todo = Todo(
        description=todo.description,
        due_date=todo.due_date,
        priority=todo.priority,
        owner_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.patch("/todos/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(create_session),
    current_user: User = Depends(get_current_user)
):

    statement = select(Todo).where(Todo.id==todo_id)
    db_todo = db.exec(statement).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail= "Todo not found")

    if db_todo.owner_id!=current_user.id:
        raise HTTPException(status_code=403, detail= "No authorisation")
    

    # Convert the incoming update model into a dictionary.
    # exclude_unset=True ensures that only fields actually sent in the request body
    # are included. Fields the user didn't send will be ignored.
    todo_data = todo.model_dump(exclude_unset=True)

    # Loop through each field provided in the request.
    # Example: {"description": "New task", "priority": "high"}
    for key, value in todo_data.items():

        # Dynamically update the corresponding attribute on the database object.
        # Example:
        # key = "description"
        # value = "New task"
        # becomes → db_todo.description = "New task"
        setattr(db_todo, key, value)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(create_session)
):

    statement = select(Todo).where(Todo.id == todo_id)
    db_todo = db.exec(statement).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(db_todo)
    db.commit()

    return {"message": "Todo deleted successfully"}