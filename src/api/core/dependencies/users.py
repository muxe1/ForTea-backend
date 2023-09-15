from common.helpers import o2auth
from core.models.users import UserDB
from fastapi import Depends, HTTPException, Request
from sqlmodel import Session, select

from ..database import engine


def get_current_user(request: Request):
    bearer = request.cookies.get('bearer')
    
    if bearer is None:
        raise HTTPException(status_code=404, detail="Not Found")
    
    payload = o2auth.decode(bearer)
    user_id: str = payload['sub']

    if user_id is None:
        raise HTTPException(status_code=404, detail="Not Found")
    
    with Session(engine) as session:
        statement = select(UserDB).where(UserDB.user_id == user_id)
        user = session.exec(statement).one_or_none()


    if user is None:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return user
    
def get_current_active_user(current_user: UserDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user