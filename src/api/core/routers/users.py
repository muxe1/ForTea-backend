import core.services.users as users
from core.dependencies.db import get_session
from core.models.users import UserAPI, UserPosts
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

router = APIRouter()

@router.get("/{userId}", response_model = UserAPI)
def get(userId: int, session: Session=Depends(get_session)) -> UserAPI: 
    return users.get(userId, session)

@router.get("/{username}", response_model = UserAPI)
def get_by_username(username: str, session: Session=Depends(get_session)) -> UserAPI: 
    return users.get_by_username(username, session)

@router.get("/{userId}/posts", response_model = UserPosts)
def get_all_posts(userId: int, offset: int = 0, limit: int = Query(default=100, lte=100), session: Session=Depends(get_session)) -> UserPosts:
    return users.get_all_posts(userId, session, offset, limit)


