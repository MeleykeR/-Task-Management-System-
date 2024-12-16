from pydantic import BaseModel
from datetime import date
from typing import Optional

# Base model for Task
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None  # Optional description
    priority: Optional[str] = "Medium"  # Default priority is 'Medium'
    due_date: Optional[date] = None  # Due date for the task

# Task model including ID (used for reading tasks)
class Task(TaskBase):
    id: int
    created_at: date
    updated_at: Optional[date] = None

    class Config:
        orm_mode = True  # Allows compatibility with ORM objects

# Example: Task Creation Model
class TaskCreate(TaskBase):
    pass

# Example: Task Update Model
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
