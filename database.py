from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Task
import crud

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management System"}

@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return tasks

@app.post("/tasks/")
def create_task(title: str, description: str = None, db: Session = Depends(get_db)):
    return crud.create_task(db, title=title, description=description)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, completed: bool, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
