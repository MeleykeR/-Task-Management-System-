from models.user import User  # Assuming 'Person' has been renamed to 'User'
from enum import Enum
from typing import Optional

# Enum for Manager Roles
class ManagerRole(str, Enum):
    TEAM_LEAD = 'team_lead'
    PROJECT_MANAGER = 'project_manager'
    DEPARTMENT_HEAD = 'department_head'

# Enum for Manager Qualification Levels (analogous to academic ranks)
class QualificationLevel(str, Enum):
    JUNIOR = 'junior'
    SENIOR = 'senior'
    EXPERT = 'expert'

# TeamLead (Manager) Model inherits from User
class TeamLead(User):
    role: ManagerRole  # Role of the manager (e.g., team lead, project manager)
    qualification_level: Optional[QualificationLevel] = None  # Qualification level (optional)

    class Config:
        orm_mode = True  # For compatibility with ORM like SQLAlchemy
