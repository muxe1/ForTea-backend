from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text, UniqueConstraint
from datetime import datetime
from typing import Union
        
class postLikeDB(SQLModel, table=True):
    __tablename__ = "postLikes"
    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="one_like_one_post_constraint_"),
    )

    id: int = Field(nullable=False, primary_key=True)
    post_id: int = Field(foreign_key="Posts.id")
    user_id: int = Field(foreign_key="Users.id")
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