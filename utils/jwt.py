import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class Jwt:
    @staticmethod
    def generate_token(user_id: int) -> str:
        payload = {"user_id": user_id}
        token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
        return token

    @staticmethod
    def verify_token(token: str = Depends(HTTPBearer())) -> int:
        try:
            payload = jwt.decode(token.credentials, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGORITHM')])
            return payload
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")