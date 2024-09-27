from sqlalchemy.orm import Session
import bcrypt
from db.models.user_model import UserModel
from utils.jwt import Jwt
from schemas.auth import SessionAuth
from datetime import datetime, timedelta

class AuthUseCase:
    def __init__(self, db: Session):
        self.db = db

    def start_sesion(self, email: str, password: str):
        user = self.db.query(UserModel).filter_by(email=email).first()
        if not user:
            return None

        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            expires_in: int = 120
            now = datetime.now()
            exp = now + timedelta(minutes=expires_in)

            return SessionAuth( user=user,  token= Jwt.generate_token(user.id, expires_in), exp = exp)
            #return Jwt.generate_token(user.id)


        return None