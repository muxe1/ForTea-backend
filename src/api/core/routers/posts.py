from core.dependencies.db import get_session
from core.dependencies.users import get_current_active_user
from core.models.posts import PostAPI, PostCreate
from core.models.users import UserDB
from core.services import posts
from fastapi import APIRouter, Depends
from sqlmodel import Session


router = APIRouter()


@router.post("", response_model = PostAPI)
def create(post: PostCreate, user: UserDB = Depends(get_current_active_user), session: Session=Depends(get_session)) -> PostAPI: 
    return posts.create(session, post, user)

@router.get("/{postId}", response_model = PostAPI)
def get(postId: int, session: Session=Depends(get_session)) -> PostAPI: 
    return posts.get(postId, session)

@router.get("/{postId}/comments", response_model = PostAPI)
def get_comments(postId: int, offset: int, limit: int, session: Session=Depends(get_session)) -> PostAPI: 
    return posts.get_comments(postId, offset, limit, session)

@router.put("/{postId}", response_model = PostAPI)
def update(postId: int, post: PostCreate, user: UserDB = Depends(get_current_active_user), session: Session=Depends(get_session)) -> PostAPI:
    return posts.update(postId, post, session)

