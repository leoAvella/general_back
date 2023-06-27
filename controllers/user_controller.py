from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from schemas.user import User, UserCreate, UserParams
from schemas.table import TableResponse
from use_cases.user_use_case import UserUseCase
from utils.jwt import Jwt

router = APIRouter(prefix='/user', tags=["User"] )

@router.get('/{id}', response_model=User)
def get_user(id: int, db: Session = Depends(database.get_db_connection), jwt = Depends(Jwt.verify_token)):
    return UserUseCase(db).get_user(id)

@router.post('/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(database.get_db_connection), jwt = Depends(Jwt.verify_token)):
    return UserUseCase(db).create_user(user)

@router.get('/all/', response_model=TableResponse)
def get_users(params: UserParams = Depends(), db: Session = Depends(database.get_db_connection), jwt = Depends(Jwt.verify_token)):
    return UserUseCase(db).get_users(params)
