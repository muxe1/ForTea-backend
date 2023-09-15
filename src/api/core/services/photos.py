from core.utils.photos import Photo, Photos
from fastapi import UploadFile
from sqlmodel import Session


def upload(photo: UploadFile, session: Session): 
    _photo = Photo(session).create()
    _photo.upload(photo)   
    return _photo.to_api()

def get_by_photo_id(photo_id: int, session: Session): 
    return Photos(session).get_by_photo_id(photo_id).to_api()