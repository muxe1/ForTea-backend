from core.dependencies.db import get_session
from core.dependencies.users import get_current_active_user
from core.models.comments import CommentAPI, CommentCreate, commentCommentsAPI
from core.models.postComments import postCommentAPI
from core.models.users import UserDB
from core.services import comments
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

router = APIRouter()

@router.post("", response_model = CommentAPI)
def create_comment(comment: CommentCreate, user: UserDB = Depends(get_current_active_user), session: Session=Depends(get_session)) -> CommentAPI: 
    return comments.create(comment, user, session)

@router.get("/{commentId}", response_model = CommentAPI)
def get(commentId: int, session: Session=Depends(get_session)) -> CommentAPI: 
    return comments.get(commentId, session)

@router.post("/{commenId}/comments", response_model = CommentAPI)
def add_comment(mainCommentId: int, commentId: int, user: UserDB = Depends(get_current_active_user), session: Session=Depends(get_session)) -> CommentAPI: 
    return comments.add_comment(mainCommentId, commentId, user, session)

@router.get("/{commentId}/comments", response_model = commentCommentsAPI)
def get_all(commentId: int, offset: int = 0, limit: int = Query(default=100, lte=100), session: Session=Depends(get_session)) -> commentCommentsAPI: 
    return comments.get_all(commentId, offset, limit, session)


# @router.get("/{postId}/comments", response_model = postCommentAPI)
# def get_all(postId: int, offset: int = 0, limit: int = Query(default=10, lte=10), session: Session=Depends(get_session)) -> postCommentAPI: 
#     return comments.get_all(postId, offset, limit, session)



# @router.put("/{postId}/comments/{commentId}", response_model = CommentAPI)
# def update(postId: int, comment: CommentCreate, user: UserDB = Depends(get_current_active_user), session: Session=Depends(get_session)) -> CommentAPI: 
#     return comments.update(postId, comment, user, session)