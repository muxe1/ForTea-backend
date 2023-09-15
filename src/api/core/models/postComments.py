from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text, Relationship
from datetime import datetime
from typing import Union, List
from core.models.comments import CommentAPI


class postCommentAPI(SQLModel):
    post_id: int = Field(gt=100000000, lt=999999999)
    comment: CommentAPI
    
class postCommentsAPI(SQLModel):
    post_id: int = Field(gt=100000000, lt=999999999)
    comments: List[CommentAPI]
    
class postCommentsDB(SQLModel, table=True):
    __tablename__ = "postComments"
    
    id: int = Field(nullable=False, primary_key=True)
    post_id: int = Field(foreign_key="Posts.id")
    comment_id: int = Field(foreign_key="Comments.id")
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
    comment: "CommentDB" = Relationship(back_populates="post")
    post: "PostDB" = Relationship(back_populates="comments")