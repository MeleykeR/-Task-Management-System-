from pydantic import BaseModel
from typing import Optional
from models.task_assignee import TaskAssignee  # Assuming TaskAssignee replaces Student

# TaskGroup Model
class TaskGroup(BaseModel):
    code: str  # Unique identifier for the task group (e.g., team code)
    leader: Optional[TaskAssignee] = None  # Leader of the task group, optional

    class Config:
        orm_mode = True  # For compatibility with ORMs like SQLAlchemy
