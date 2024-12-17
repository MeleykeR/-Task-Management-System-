from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Input schema for adding a new user
class UserInputAdd(BaseModel):
    name: str = Field(..., max_length=50, description="Name of the user")
    role: str = Field(..., max_length=30, description="Role of the user (e.g., developer, designer)")
    email: EmailStr = Field(..., description="Email address of the user")


# Input schema for updating an existing user
class UserInputUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50, description="Updated name of the user")
    role: Optional[str] = Field(None, max_length=30, description="Updated role of the user")
    email: Optional[EmailStr] = Field(None, description="Updated email address of the user")


# Output schema for searching and retrieving users
class UserOutputSearch(BaseModel):
    id: int = Field(..., description="ID of the user")
    name: str = Field(..., description="Name of the user")
    role: str = Field(..., description="Role of the user")
    email: EmailStr = Field(..., description="Email address of the user")

    class Config:
        orm_mode = True
