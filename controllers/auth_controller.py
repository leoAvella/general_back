from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from use_cases.auth_use_case import AuthUseCase


router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post('/login')
def login(email: str, password: str, db: Session = Depends(database.get_db_connection)):
    jwt =   AuthUseCase(db).start_sesion(email, password)
    if jwt:
        return {'message': 'Inicio de sesión exitoso', 'jwt': jwt}
    else:
        raise HTTPException(status_code=401, detail='Credenciales inválidas')