from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    email_verified_at = Column(String)
    password = Column(String, nullable=False)
    remember_token = Column(String)
    updated_at = Column(String)
    status = Column(String)
    image = Column(String)
