from core.models.posts import PostAPI, PostBase, PostCreate
from core.models.users import UserDB
from core.utils.posts import Post, Posts
from sqlmodel import Session
from core.models.postComments import postCommentsAPI
from core.utils.comments import Comments
from common.helpers import counters

def create(session: Session, post: PostCreate, user: UserDB) -> PostAPI: 
    return Post(session, post).create(user).to_api()

def get(post_id: int, session: Session) -> PostAPI: 
    return Posts(session).get(post_id).to_api()

def update(post_id: int, post_update: PostBase, session: Session) -> PostAPI:
    return Posts(session).get(post_id).update(post_update).to_api()

def get_comments(post_id: int, offset: int, limit: int, session: Session) -> postCommentsAPI:
    comments = []
    for comment in Posts(session).get(post_id).post.comments:
        comments.append(Comments(session).get_by_id(comment.id).to_api())
    return postCommentsAPI(post_id=post_id, comments=counters.sampling(comments, offset, limit))

# def add_comments(post_id: int, comment_id: int, session: Session) -> CommentAPI:
#     comment = Posts(session).get(post_id).add_comment(comment_id).to_api()
#     return CommentAPI(comment_id=comment_id, comment=Comment(text=comment.text,
#                                                       photos=[i.photo_id for i in comment.photos]))