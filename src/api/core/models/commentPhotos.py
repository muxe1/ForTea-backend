from datetime import datetime

from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text


class commentPhotosDB(SQLModel, table=True):
    __tablename__ = "commentPhotos"
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
    comment_id: int = Field(foreign_key="Comments.id")

    photo: "PhotoDB" = Relationship()
    comment: "CommentDB" = Relationship(back_populates="photos")