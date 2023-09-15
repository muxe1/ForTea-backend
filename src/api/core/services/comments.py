from common.helpers import counters
from core.models.comments import CommentAPI, CommentCreate, commentCommentsAPI
from core.models.users import UserDB
from core.utils.comments import Comment, Comments
from sqlmodel import Session


def create(comment: CommentCreate, user: UserDB, session: Session) -> CommentAPI:
    return Comment(session).create(comment, user).to_api()

def add_comment(main_comment_id: int, comment_id: CommentCreate, user: UserDB, session: Session) -> CommentAPI:
    main_comment = Comments(session).get_by_comment_id(main_comment_id)
    comment = Comments(session).get_by_comment_id(comment_id)
    return main_comment.add_comment(comment).to_api()

def get(comment_id: int, session: Session) -> CommentAPI: 
    return Comment(session).get(comment_id).to_api()

def get_all(comment_id: int, offset: int, limit: int, session: Session) -> commentCommentsAPI: 
    all_coments_to_comment = Comment(session).get_all_for_comment(comment_id, offset, limit)
    comments = []
    for comment in all_coments_to_comment:
        comments.append(Comments(session).get_by_id(comment.id).to_api())
    return commentCommentsAPI(comment_id=comment_id, comments=counters.sampling(comments, offset, limit))