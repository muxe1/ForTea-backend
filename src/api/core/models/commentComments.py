from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text, UniqueConstraint
from datetime import datetime

class commentCommentsDB(SQLModel, table=True):
    __tablename__ = "commentComments"
    __table_args__ = (
        UniqueConstraint("comment_id", "main_comment_id", name="one_comment_one_main_comment_constraint_"),
        UniqueConstraint("main_comment_id", "comment_id", name="one_main_comment_one_comment_constraint_"),
    )
    
    id: int = Field(nullable=False, primary_key=True)
    comment_id: int = Field(foreign_key="Comments.id")
    main_comment_id: int = Field(foreign_key="Comments.id")
    
    created_datetime: datetime | None = Field(sa_column=Column(
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
    
    