from typing import List, Self

from core.models.commentComments import commentCommentsDB
from core.models.commentPhotos import commentPhotosDB
from core.models.comments import Comment as CommentModel, CommentAPI, CommentCreate, CommentDB, commentCommentsAPI
from core.models.users import UserDB
from core.utils.photos import Photos
from fastapi import HTTPException
from sqlmodel import Session, select


class Comment():
    def __init__(self, session: Session, comment: CommentDB=None):
        self.comment = comment
        self.session = session
        
    def to_api(self) -> CommentAPI:
        return CommentAPI(comment_id=self.comment.comment_id,
                          comment=CommentModel(text=self.comment.text,
                                               photos=[i.photo_id for i in self.comment.photos]))
    
    def create(self, comment: CommentCreate, user: UserDB) -> Self:
        _comment = CommentDB(text=comment.text, user_id=user.id)
        self.session.add(_comment)
        self.session.commit()
        self.session.refresh(_comment)
        
        for i in comment.photos:  
            photo__id = Photos(self.session).get_by_photo_id(i).photo.id  
            self.session.add(commentPhotosDB(comment_id=_comment.id, photo_id=photo__id))
        
        self.session.commit()    
             
        return Comment(self.session, _comment)
    
    def add_comment(self, comment: Self) -> Self:
        _comment = commentCommentsDB(comment_id=comment.comment.id, main_comment_id=self.comment.id)
        self.session.add(_comment)
        self.session.commit()
        return self
    
    
    def get(self, comment_id: int) -> Self:
        statement = select(CommentDB).where(CommentDB.comment_id == comment_id)
        comment = self.session.exec(statement).one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment Not Found") 
        return Comment(self.session, comment)
        
    def get_all_for_comment(self, comment_id, offset, limit) -> List[commentCommentsDB]:
        statement = select(commentCommentsDB).where(CommentDB.comment_id == comment_id)
        comments = self.session.exec(statement).all()
        return comments
    
     
class Comments(Comment):
    def __init__(self, session: Session, comments: List[CommentDB]=None):
        self.session = session
        self.comments = comments
        
    def to_api(self) -> List[commentCommentsAPI]:
        comments = []
        for comment in self.comments:
            comments.append(Comment(self.session, comment).to_api())
        
        return commentCommentsAPI(comment.comment_id, comments=comments)
                                                                
    def get_by_id(self, id: int) -> Comment: 
        statement = select(CommentDB).where(CommentDB.id == id)
        comment = self.session.exec(statement).one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail="comment Not Found") 
        return Comment(self.session, comment)
    
    def get_by_comment_id(self, comment_id: int) -> Comment: 
        statement = select(CommentDB).where(CommentDB.comment_id == comment_id)
        comment = self.session.exec(statement).one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail="comment Not Found") 
        return Comment(self.session, comment)
    
    

