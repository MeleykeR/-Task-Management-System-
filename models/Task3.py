# Example of a class using a constructor, without using BaseModel
class Project:
    def __init__(self, id: int, name: str, code: str, estimated_hours: int, budget: float = None):
        self.id = id  # Unique identifier for the project
        self.name = name  # Name of the project
        self.code = code  # Unique code for the project (e.g., PROJ123)
        self.estimated_hours = estimated_hours  # Estimated hours for completion
        self.budget = budget  # Optional budget for the project
