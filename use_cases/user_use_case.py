from sqlalchemy.orm import Session
from datetime import datetime
import bcrypt
from schemas.user import UserCreate, User, UserParams,UserUpdate
from db.models.user_model import UserModel
from utils.query_utils import QuertUtils
from schemas.table import  TableResponse


class UserUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.query_utils = QuertUtils(db)

    def get_users(self, params: UserParams)->TableResponse:
        return self.query_utils.get_data_table(params, UserModel, User)

    
    def get_user(self, id: int):
        return self.db.query(UserModel).filter_by(id=id).first()

    def create_user(self, user: UserCreate):
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        user.password = hashed_password.decode("utf-8")     
        return self.query_utils.save_model(user.dict(), UserModel)

    def update_user(self, id: int, user: UserUpdate):
        return self.query_utils.update_model(id, user.dict(), UserModel)
