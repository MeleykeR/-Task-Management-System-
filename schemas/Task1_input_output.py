from pydantic import BaseModel
from datetime import date, datetime
from models.person import Gender
from models.student import Student  # In this context, you would use a 'User' model instead of 'Student' for the task system.

class UserInputAdd(BaseModel):
    '''Input data for adding a new user.'''
    
    # Required fields
    first_name: str
    last_name: str
    role: str  # For example: "developer", "manager", "designer"

    # Optional fields
    gender: Gender | None = None
    birth_date: date | None = None
    team_id: int | None = None  # Optional: Assign the user to a team (if applicable)

class UserInputUpdate(BaseModel):
    '''Input data for updating an existing user.'''
    
    # Fields that are optional to update
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    gender: Gender | None = None
    birth_date: date | None = None
    team_id: int | None = None

# Example of how to search for users and output relevant fields
class UserOutputSearch(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: str
    team_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None
    
    class Config:
        # Hide certain fields from the output
        exclude = {"updated_at"}

class TaskInputAdd(BaseModel):
    '''Input data for adding a new task.'''
    
    name: str
    description: str | None = None
    assigned_to: int  # user_id that the task is assigned to
    due_date: date
    status: str  # Example: "pending", "in_progress", "completed"

class TaskInputUpdate(BaseModel):
    '''Input data for updating an existing task.'''
    
    name: str | None = None
    description: str | None = None
    assigned_to: int | None = None
    due_date: date | None = None
    status: str | None = None

class TaskOutputSearch(BaseModel):
    id: int
    name: str
    description: str | None
    assigned_to: int  # user_id of the person the task is assigned to
    due_date: date
    status: str
    created_at: datetime
    updated_at: datetime | None = None
    
    class Config:
        # Hide created_at for output
        exclude = {"created_at"}

class TeamInputAdd(BaseModel):
    '''Input data for adding a new team.'''
    
    code: str
    leader_id: int  # user_id that is the leader of the team

class TeamInputUpdate(BaseModel):
    '''Input data for updating an existing team.'''
    
    code: str | None = None
    leader_id: int | None = None

class TeamOutputSearch(BaseModel):
    id: int
    code: str
    leader_id: int
    created_at: datetime
    updated_at: datetime | None = None
    
    class Config:
        # Hide created_at for output
        exclude = {"created_at"}

# JournalInputUpdate (Task Management Context)
class TaskUpdate(BaseModel):
    task_name: str | None = None
    assigned_to: int | None = None
    due_date: date | None = None
    status: str | None = None

# Output search for Task
class TaskOutputSearch(BaseModel):
    id: int
    task_name: str
    description: str | None
    assigned_to: int
    due_date: date
    status: str
    created_at: datetime
    updated_at: datetime | None = None
    
    class Config:
        # Exclude created_at from the output if required
        exclude = {"created_at"}
