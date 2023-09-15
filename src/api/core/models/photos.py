from datetime import datetime
from typing import List, Self

from common.helpers import id_generator
from core.models.postPhotos import postPhotosDB
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text


class PhotoBase(SQLModel):
    s3: int = Field(default_factory = id_generator.create, gt=100000000, lt=999999999)
    
class PhotoCreate(PhotoBase):
    ...
    class Config:
        orm_mode = True

class Photo(SQLModel):
    s3: int
    class Config:
        orm_mode = True
        
class PhotoAPI(SQLModel):
    photo_id: int = Field(gt=100000000, lt=999999999)
    photo: Photo
    
    class Config:
        orm_mode = True
        
class PhotoDB(PhotoBase, table=True):
    __tablename__ = "Photos"
    id: int = Field(primary_key=True)
    photo_id: int = Field(default_factory = id_generator.create, gt=100000000, lt=999999999)
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
    
    posts: List[postPhotosDB] = Relationship(back_populates="photo")
    user: 'UserDB' = Relationship(back_populates="photo")
    
    @classmethod
    def to_api(cls, self: Self) -> PhotoAPI:
        return PhotoAPI(photo_id=self.photo_id,
                        photo=Photo(s3=self.s3))

    
    