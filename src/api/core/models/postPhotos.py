from datetime import datetime
from typing import Union

from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text


class postPhotosDB(SQLModel, table=True):
    __tablename__ = "postPhotos"
    id: int = Field(nullable=False, primary_key=True)
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
    photo_id: int = Field(foreign_key="Photos.id")
    post_id: int = Field(foreign_key="Posts.id")
    
    photo: "PhotoDB" = Relationship(back_populates="posts")
    post: "PostDB" = Relationship(back_populates="photos")