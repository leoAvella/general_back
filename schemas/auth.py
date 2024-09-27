
from pydantic import BaseModel,Field
from .user import User
from datetime import datetime

class AuthLogin(BaseModel):
    email: str  
    password: str

class SessionAuth(BaseModel):
    user: User
    token: str
    exp: datetime