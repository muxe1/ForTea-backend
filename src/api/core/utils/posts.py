from typing import List, Self

from core.models.comments import CommentDB
from core.models.photos import PhotoDB
from core.models.postComments import postCommentsDB
from core.models.postPhotos import postPhotosDB
from core.models.posts import Post as PostModel
from core.models.posts import PostAPI, PostCreate, PostDB
from core.models.users import UserDB
from core.utils.comments import Comment
from fastapi import HTTPException
from sqlmodel import Session, select


class Post():
    def __init__(self, session: Session, post: PostDB=None):
        self.post = post
        self.session = session
    
    def to_api(self) -> PostAPI:
        return PostAPI(post_id=self.post.post_id,
                       post=PostModel(title=self.post.title,
                                      text=self.post.text,
                                      photos=[i.photo.photo_id for i in self.post.photos]))
        
    def create(self, user: UserDB) -> Self:
        post = PostDB(user_id=user.id, title=self.post.title, text=self.post.text)
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        
        for i in self.post.photos:
            statement = select(PhotoDB).where(PhotoDB.photo_id == i)
            photo = self.session.exec(statement).one_or_none()
            if not photo:
                raise HTTPException(status_code=404, detail="Photo Not Found") 
            
            postPhoto = postPhotosDB(post_id=post.id, photo_id=photo.id)
            self.session.add(postPhoto)
            
        self.session.commit()
        return Post(self.session, post)
    
    def update(self, post_update: PostCreate) -> Self:
        statement = select(PostDB).where(PostDB.post_id == self.post.post_id)
        post = self.session.exec(statement).one()
        
        if post_update.title:        
            post.title = post_update.title
        
        if post_update.text:
            post.text = post_update.text
        
        if post_update.photos:
            for photo_id in post_update.photos:
                statement = select(postPhotosDB).where(postPhotosDB.post_id == self.post.id)
                _postPhotos = self.session.exec(statement).all()
                for postPhoto in _postPhotos:
                    statement = select(PhotoDB).where(PhotoDB.photo_id == photo_id)  
                    photo = self.session.exec(statement).one()

                    postPhoto.photo_id = photo.id
                    
                    self.session.add(postPhoto)
                    self.session.commit()
                    self.session.refresh(postPhoto)


            
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return self        
    
    def add_comment(self, comment_id: int, session: Session) -> Comment:
        statement = select(CommentDB).where(CommentDB.comment_id == comment_id)
        comment = self.session.exec(statement).one()
        comment = postCommentsDB(post_id=self.post.id, comment_id=comment.id)
        self.session.add(comment)
        return Comment(self.session, comment)
    
class Posts():
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def get_all_by_username(username: int, session: Session) -> List[PostAPI]:
        posts: List[PostAPI] = []
        statement = select(PostDB).where(UserDB.username == username)
        _posts = session.exec(statement).all()
        if len(_posts) > 0:  
            for _post in _posts:
                posts.append(PostAPI.from_orm(_post, {"post": PostCreate.from_orm(_post)}))
        return posts
    
    def get(self, post_id: int) -> Post: 
        statement = select(PostDB).where(PostDB.post_id == post_id)
        post = self.session.exec(statement).one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post Not Found") 
        return Post(self.session, post)