from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field
from .table import TableParams 


class UserUpdate(BaseModel):
    name: str
    image: Optional[str]


class UserCreate(BaseModel):
    name: str
    email: str  
    password: str
    image: Optional[str]
    
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
