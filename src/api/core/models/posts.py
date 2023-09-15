from datetime import datetime
from typing import Any, List, Union, Self
from core.models.postComments import postCommentsDB
from common.helpers import id_generator
from core.models.postPhotos import postPhotosDB
from pydantic import constr
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text

class PostBase(SQLModel):
    title: constr(max_length=100)
    text: constr(max_length=2000)

class Post(PostBase):
    photos: List[int]
    class Config:
        orm_mode = True
   
class PostCreate(PostBase):
    photos: List[int]
    class Config:
        orm_mode = True

class PostAPI(SQLModel):
    post_id: int = Field(gt=100000000, lt=999999999)
    post: Post
    
    class Config:
        orm_mode = True

class PostDB(PostBase, table=True):
    __tablename__ = "Posts"
    id: int = Field(nullable=False, primary_key=True)
    user_id: int = Field(foreign_key="Users.id")
    post_id: int = Field(default_factory = id_generator.create, gt=100000000, lt=999999999)
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
    comments: List[postCommentsDB] = Relationship(back_populates="post")
    photos: List[postPhotosDB] = Relationship(back_populates="post")
    user: "UserDB" = Relationship(back_populates="posts") 
    