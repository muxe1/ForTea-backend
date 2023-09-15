from datetime import datetime
from typing import List

from common.helpers import id_generator
from pydantic import constr
from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text, Relationship
from core.models.commentPhotos import commentPhotosDB
from core.models.commentComments import commentCommentsDB
from sqlalchemy.orm import declarative_base, relationship

class CommentBase(SQLModel):
    text: constr(min_length=1, max_length=1024)

class Comment(CommentBase):
    photos: List[int]
    class Config:
        orm_mode = True
         
class CommentCreate(SQLModel):
    text: constr(min_length=1, max_length=1024)
    photos: List[int]
    class Config:
        orm_mode = True
        
class CommentAPI(SQLModel):
    comment_id: int = Field(gt=100000000, lt=999999999)
    comment: Comment
    
    class Config:
        orm_mode = True

class commentCommentsAPI(SQLModel):
    comment_id: int = Field(gt=100000000, lt=999999999)
    comments: List[CommentAPI]
    
class CommentDB(CommentBase, table=True):
    __tablename__ = "Comments"
    id: int = Field(nullable=False, primary_key=True)
    user_id: int = Field(foreign_key="Users.id")
    comment_id: int = Field(default_factory = id_generator.create, gt=100000000, lt=999999999)
    created_datetime:datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_datetime: datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    
    post: "postCommentsDB" = Relationship(back_populates="comment")
    main_comment: 'CommentDB' = Relationship(
                                            back_populates="comments",
                                            link_model=commentCommentsDB,
                                            sa_relationship_kwargs=dict(
                                                primaryjoin="Comments.c.id==commentComments.c.main_comment_id",
                                                secondaryjoin="Comments.c.id==commentComments.c.comment_id",
                                            )
                                            ) 
    comments: 'CommentDB' = Relationship(
                                        back_populates="main_comment",
                                        link_model=commentCommentsDB,
                                        sa_relationship_kwargs=dict(
                                            primaryjoin="Comments.c.id==commentComments.c.comment_id",
                                            secondaryjoin="Comments.c.id==commentComments.c.main_comment_id",
                                        )
                                        ) 
    
    photos: List[commentPhotosDB] | None  = Relationship(back_populates="comment")
    
    