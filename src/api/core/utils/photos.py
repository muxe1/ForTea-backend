from typing import Self

from core.models.photos import Photo as PhotoModel
from core.models.photos import PhotoAPI, PhotoDB
from fastapi import HTTPException, UploadFile
from sqlmodel import Session, select

from ..database import s3


class Photo():
    def __init__(self, session: Session, photo: PhotoDB=None):
        self.photo = photo
        self.session = session
        
    def to_api(self) -> PhotoAPI:
        if not self.photo.s3:
            self.photo.s3 = []
        return PhotoAPI(photo_id=self.photo.photo_id,
                        photo=PhotoModel(s3=self.photo.s3))
    
    def create(self) -> Self:
        _photo = PhotoDB()
        
        self.session.add(_photo)
        self.session.commit()

        return Photo(self.session, _photo)
    
    def upload(self, photo: UploadFile): 
        s3.upload_fileobj(photo.file, 'ft-pht', f'photos/{self.photo.s3}.png')  
        return {"status": "success"}
     
class Photos(Photo):
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, id: int) -> Photo: 
        statement = select(PhotoDB).where(PhotoDB.id == id)
        photo = self.session.exec(statement).one_or_none()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo Not Found") 
        return Photo(self.session, photo)
    
    def get_by_photo_id(self, photo_id: int) -> Photo: 
        statement = select(PhotoDB).where(PhotoDB.photo_id == photo_id)
        photo = self.session.exec(statement).one_or_none()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo Not Found") 
        return Photo(self.session, photo)
    
    

