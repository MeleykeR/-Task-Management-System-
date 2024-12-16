from models.user import User  

# Example of inheritance: TaskAssignee is a subclass of User
class TaskAssignee(User):
    role: str  # Role of the assignee (e.g., 'developer', 'manager', etc.)
    joined_year: int  # The year when the user joined the task management system
