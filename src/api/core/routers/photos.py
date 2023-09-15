from core.dependencies.db import get_session
from core.models.photos import PhotoAPI
from core.services import photos
from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session

router = APIRouter()

@router.post("", response_model = PhotoAPI)
def upload(photo: UploadFile, session: Session=Depends(get_session)): 
    return photos.upload(photo, session)

@router.get("/{photoId}", response_model = PhotoAPI)
def get_by_photoId(photoId: int, session: Session=Depends(get_session)): 
    return photos.get_by_photo_id(photoId, session)

