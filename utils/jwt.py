from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class Jwt:
    @staticmethod
    def generate_token(user_id: int, expires_in: int = 1) -> str:
        now = datetime.utcnow()
        exp = now + timedelta(minutes=expires_in)
        payload = {"user_id": user_id, "exp": exp}
        token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
        return token

    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> int:
        try:
            # Decodifica el token JWT
            payload = jwt.decode(credentials.credentials, os.getenv('JWT_SECRET_KEY'),
                                 algorithms=[os.getenv('JWT_ALGORITHM')])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")