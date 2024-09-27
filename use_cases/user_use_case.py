from datetime import datetime
from typing import Optional, Type

import bcrypt
from sqlalchemy.orm import Session

from db.models.user_model import UserModel
from schemas.table import TableResponse
from schemas.user import User, UserCreate, UserParams, UserUpdate
from utils.query_utils import QuertUtils


class UserUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.query_utils = QuertUtils(db)

    def get_users(self, params: UserParams)->TableResponse:
        return self.query_utils.get_data_table(params, UserModel, User)
 
    def get_user(self, id: int) -> Optional[UserModel]:
        return self.query_utils.get_model_by_id(id, UserModel)

    def create_user(self, user: UserCreate):
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        user.password = hashed_password.decode("utf-8")     
        return self.query_utils.save_model(user.dict(), UserModel)

    def update_user(self, id: int, user: UserUpdate):
        return self.query_utils.update_model(id, user.dict(), UserModel)
