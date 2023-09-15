
import core.services.users as users
from core.dependencies.db import get_session
from core.dependencies.users import get_current_active_user, get_current_user
from core.models.users import UserAPI, UserDB, UserUpdate
from core.utils.users import User
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()

@router.get("", response_model = UserAPI)
def get(user: UserDB=Depends(get_current_user), session: Session=Depends(get_session)) -> UserAPI: 
    return User(session, user).to_api()

@router.put("", response_model = UserAPI)
def update(user_data_for_update: UserUpdate, current_user: UserDB = Depends(get_current_active_user), session: Session=Depends(get_session)) -> UserAPI:
    return users.update(current_user, user_data_for_update, session)

@router.put("/photo", response_model = UserAPI)
def update_photo(photo_id: int, current_user: UserDB = Depends(get_current_active_user), session: Session=Depends(get_session)) -> UserAPI:
    return users.update_photo(photo_id, current_user, session)