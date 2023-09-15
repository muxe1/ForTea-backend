from datetime import datetime
from typing import List

from common.helpers import id_generator
from core.dependencies.db import get_session
from core.models.photos import PhotoDB
from core.models.posts import PostAPI, PostDB
from pydantic import EmailStr, constr, validator, BaseModel
from sqlmodel import (TIMESTAMP, Column, Field, Relationship, Session,
                      SQLModel, text)


from fastapi import HTTPException
from sqlmodel import Session, select


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    
class UserCreate(BaseModel):
    email: EmailStr = Field(unique=True)
    password: constr(min_length=8, max_length=64, regex="((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})") 
         
    class Config:
        orm_mode = True
    
    def validate(cls, self):
        session: Session = next(get_session())
        Validator(session).check_email_for_create_or_update(self['email'])
        return UserCreate(**self)
      
class User(UserBase):
    username: constr(min_length=3, max_length=20) | None = Field(unique=True)
    first_name: constr(min_length=3, max_length=20) | None
    photo_id: int | None
    
    class Config:
        orm_mode = True
    
        
class UserUpdate(SQLModel):
    username: constr(min_length=3, max_length=20) = Field(None, unique=True)
    first_name: str = Field(None)
    
    def validate(cls, self):
        session: Session = next(get_session())
        Validator(session).check_username_for_create_or_update(self['username'])
        return UserUpdate(**self)
    
class UserAPI(SQLModel):
    user_id: int = Field(gt=100000000, lt=999999999)
    user: User   
    
class UserLogin(BaseModel):
    email: EmailStr = Field(unique=True)
    password: constr(min_length=8, max_length=64, regex="((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})") 
    
    def validate(cls, self):
        session: Session = next(get_session())
        Validator(session).check_email_for_login(self['email'])
        return UserLogin(**self)
    
class UserDB(UserBase, table=True):
    __tablename__ = "Users"
    id: int = Field(nullable=False, primary_key=True)
    user_id: int = Field(default_factory = id_generator.create)
    password_hash: str
    username: constr(min_length=3, max_length=20) | None = Field(unique=True)
    first_name: str | None
    created_at: datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_at: datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    is_active: bool = Field(default=True)
    
    photo_id: int | None = Field(nullable=True, foreign_key="Photos.id")
    photo: PhotoDB | None = Relationship(back_populates="user")
    posts: List[PostDB] = Relationship(back_populates="user")


class UserPosts(SQLModel):
    user_id: int
    posts: List[int] | List
     
class Token(SQLModel):
    access_token: str

class TokenData(SQLModel):
    user_id: str | None = None
    

class Validator():
    def __init__(self, session: Session):
        self.session = session
    
    def check_email_for_login(self, email):
        statement = select(UserDB).where(UserDB.email == email)
        user = self.session.exec(statement).one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
    def check_email_for_create_or_update(self, email):
        statement = select(UserDB).where(UserDB.email == email)
        user = self.session.exec(statement).one_or_none()
        if user:
            raise HTTPException(status_code=409, detail="this email already exists")
       
    def check_username_for_create_or_update(self, username):
        statement = select(UserDB).where(UserDB.username == username)
        user = self.session.exec(statement).one_or_none()
        if user:
            raise HTTPException(status_code=409, detail="this username already exists")