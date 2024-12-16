from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Model for creating a new Task/Project entry
class TaskInputAdd(BaseModel):
    name: str
    description: str
    assigned_to: int  # User ID (the person assigned to the task)
    due_date: date
    status: str  # Pending, In Progress, Completed
    project_id: int  # Link to the project if relevant

# Model for updating an existing Task/Project entry
class TaskInputUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[int] = None  # User ID for updating assignee
    due_date: Optional[date] = None
    status: Optional[str] = None  # Status updates
    project_id: Optional[int] = None  # Optionally link to a project

# Model for fetching task/project details (output)
class TaskOutputSearch(BaseModel):
    id: int
    name: str
    description: str
    assigned_to: int  # User ID
    due_date: date
    status: str
    project_id: int  # Linked project
    created_at: datetime
    updated_at: datetime
