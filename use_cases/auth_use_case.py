from sqlalchemy.orm import Session
import bcrypt
from db.models.user_model import UserModel
from utils.jwt import Jwt

class AuthUseCase:
    def __init__(self, db: Session):
        self.db = db

    def start_sesion(self, email: str, password: str):
        user = self.db.query(UserModel).filter_by(email=email).first()
        if not user:
            return None

        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return Jwt.generate_token(user.id)
           
        
        return None