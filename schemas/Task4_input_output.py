from models.person import Person
from enum import Enum

# Enum for different roles in a task management system (e.g., Assignee, Manager)
class Role(str, Enum):
    assignee = 'assignee'
    manager = 'manager'
    team_lead = 'team_lead'

# Enum for different positions or expertise levels (could be based on job levels or seniority)
class Position(str, Enum):
    junior = 'junior'
    mid = 'mid'
    senior = 'senior'

# Inheriting from the Person class (which contains common fields like first_name, last_name, etc.)
class TeamMember(Person):
    role: Role | None = None  # Role of the team member in the project/task
    position: Position | None = None  # Position or expertise level in the company
