from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import DBConnection
from schemas.auth import AuthLogin
from use_cases.auth_use_case import AuthUseCase


router = APIRouter(prefix='/auth', tags=["Auth"])

database = DBConnection()


@router.post('/login')
def login(params: AuthLogin, db: Session = Depends(database.get_db_connection)):
    jwt =   AuthUseCase(db).start_sesion(params.email, params.password)
    if jwt:
        return {'message': 'Login successful', 'jwt': jwt}
    else:
        raise HTTPException(status_code=401, detail={'message':'Invalid username or password'})