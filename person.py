from pydantic import BaseModel, computed_field
from datetime import date
from enum import Enum
from typing import Optional

# Enum for Gender
class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'

# ABSTRACTION: Base User Model for the Task Management System
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

    # Optional parameter for gender
    gender: Optional[Gender] = None

    # Date of birth using datetime.date type
    birth_date: Optional[date] = None

    # Example of ENCAPSULATION: Logic to compute full_name
    @computed_field
    @property
    def full_name(self) -> str:
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{middle} {self.last_name}"

    # Example of ENCAPSULATION: Logic to compute age
    @property
    def age(self) -> Optional[int]:
        if self.birth_date is None:
            return None
        return date.today().year - self.birth_date.year

    # Timestamps for user creation and updates
    created_at: date
    updated_at: Optional[date] = None

    class Config:
        orm_mode = True  # For ORM compatibility
