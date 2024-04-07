from fastapi import FastAPI
from models import Todo
from auth import (
    LoginUser,
    Token,
    authenticate_user,
    fake_users_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    User,
    get_current_active_user
)
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
# docs, redoc


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def fake_streamer():
    for i in range(10):
        await asyncio.sleep(1)
        yield f"some bytes {i}"


@app.get("/")
async def root():
    return {"message": "Hello World"}

todos = []


# Create JWT token
@app.post("/token")
async def login_for_access_token(
    form_data: LoginUser  # Annotated[LoginUser, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# Get all todos
@app.get("/todos")
async def get_todos(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return {"todos": todos}


# Get single todo
@app.get("/todos/{todo_id}")
async def get_todo(
    current_user: Annotated[User, Depends(get_current_active_user)],
    todo_id: int
):
    for todo in todos:
        if todo.id == todo_id:
            return {"todo": todo}
    return {"Message": "No todos found"}


# Create a todo
@app.post("/todos")
async def create_todo(
    current_user: Annotated[User, Depends(get_current_active_user)],
    todo: Todo
):
    todos.append(todo)
    return {"message": "Todo added"}


# Update a todo
@app.put("/todos/{todo_id}")
async def update_todo(
    current_user: Annotated[User, Depends(get_current_active_user)],
    todo_id: int,
    todo_obj: Todo
):
    for todo in todos:
        if todo.id == todo_id:
            todo.id = todo_id
            todo.item = todo_obj.item
            return {"todo": todo}
    return {"Message": "No todos found"}


# Delete a todo
@app.delete("/todos/{todo_id}")
async def delete_todo(
    current_user: Annotated[User, Depends(get_current_active_user)],
    todo_id: int
):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "Todo has been deleted"}
    return {"Message": "No todos found"}


@app.get("/stream")
async def stream(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return StreamingResponse(fake_streamer())
