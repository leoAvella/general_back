from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr,Field
from .table import TableParams 


class UserUpdate(BaseModel):
    name: str
    image: Optional[str]


class UserCreate(BaseModel):
    name: str = Field(..., min_length=8, max_length=20, example="JohnDoe", description="The name must be between 8 and 20 characters.")
    email: EmailStr = Field(..., example="johndoe@example.com", description="Please provide a valid email address.")
    password: str = Field(..., example="password123", description="The password must be provided.")
    image: Optional[str] = Field(None, example="https://example.com/profile.jpg", description="Optional profile image URL.")
    
class User(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]  
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    image: Optional[str]

    class Config:
        orm_mode = True

class UserParams(User,TableParams):
    pass
