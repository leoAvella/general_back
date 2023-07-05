
from pydantic import BaseModel,Field

class AuthLogin(BaseModel):
    email: str  
    password: str

