import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from decouple import config

class Jwt:
    @staticmethod
    def generate_token(user_id: int) -> str:
        payload = {"user_id": user_id}
        token = jwt.encode(payload, config('JWT_SECRET_KEY'), algorithm=config('JWT_ALGORITHM'))
        return token

    @staticmethod
    def verify_token(token: str = Depends(HTTPBearer())) -> int:
        try:
            payload = jwt.decode(token.credentials, config('JWT_SECRET_KEY'), algorithms=[config('JWT_ALGORITHM')])
            return payload
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")