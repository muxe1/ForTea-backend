from datetime import datetime, timedelta
from typing import List, Self

from common.helpers import o2auth
from common.helpers.o2auth import create_access_token, get_password_hash
from core.models.photos import PhotoDB
from core.models.posts import PostAPI, PostDB
from core.models.users import (UserAPI, UserDB, UserLogin,
                               UserUpdate, UserCreate, User as UserSchema, Token)
from fastapi import HTTPException, Response, Request, Query
from sqlmodel import Session, select
from core.utils.photos import Photos
from common.helpers import counters
class User():
    def __init__(self, session: Session, user: UserUpdate | UserDB | UserCreate):    
        self.session: Session = session
        self.user = user

    def create(self) -> Self:
        user = UserDB(email=self.user.email, password_hash=get_password_hash(self.user.password))
        user.username = user.user_id
        self.session.add(user)
        self.session.commit()
            
        return User(self.session, user) 

    def authenticate_user(self, user: UserLogin) -> Self:
        statement = select(UserDB).where(UserDB.email == user.email)
        _user = self.session.exec(statement).one_or_none()

        if not o2auth.verify_password(user.password, _user.password_hash):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return User(self.session, _user)
    
    def register(self) -> Token:
        access_token = create_access_token(data={"sub": str(self.user.user_id)})
        return Token(access_token=access_token, token_type="bearer")

    def login(self, response: Response) -> Token:
        user = self.authenticate_user(self.user)
        access_token = create_access_token(data={"sub": str(user.user.user_id)})
        
        expires = datetime.strftime(
            datetime.utcnow() + timedelta(days=365),
            "%a, %d-%b-%Y %H:%M:%S GMT",
        )
        
        response.set_cookie(key="bearer", value=access_token, expires = expires)
        
        return Token(access_token=access_token, token_type="bearer")
 
    def logout(response: Response):
        response.delete_cookie("bearer")
        return {"status": "success"}
    
    def to_api(self):      
        if self.user.photo_id is None:
            user_photo = None
        else:
            photo = Photos(self.session).get_by_id(self.user.photo_id)
            user_photo = photo.photo.photo_id
        
        return UserAPI(user_id=self.user.user_id,
                       user=UserSchema(email=self.user.email,
                                 username=self.user.username,
                                 first_name=self.user.first_name,
                                 photo_id=user_photo
                                ))
        
    def get_all_posts(self, offset: int, limit: int) -> List[PostDB]:
        return counters.sampling(self.user.posts, offset, limit)
               
    def update(self, user_data_for_update: UserUpdate) -> Self:
        statement = select(UserDB).where(UserDB.user_id == self.user.user_id)
        user = self.session.exec(statement).one()
        
        if user_data_for_update.username is not None:
            user.username = user_data_for_update.username
            
        if user_data_for_update.first_name is not None:    
            user.first_name = user_data_for_update.first_name
            
        self.session.add(user)
        self.session.commit()
        
        self.session.refresh(user)
        
        return User(self.session, user) 

    def update_photo(self, photo_id: int) -> Self:     
        statement = select(PhotoDB).where(PhotoDB.photo_id == photo_id)
        photo = self.session.exec(statement).one_or_none()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo Not Found") 
        
        self.user.photo_id = photo.id

        self.session.add(self.user)
        self.session.commit()
        
        self.session.refresh(self.user)

        return User(self.session, self.user) 
    
    
class Users(User):
    def __init__(self, session: Session) -> User:
        self.session: Session = session
    
    def get_by_session(self, request: Request):
        access_token = request.cookies.get('bearer')
        print(o2auth.decode(access_token))
    
    def get(self, user_id) -> User: 
        statement = select(UserDB).where(UserDB.user_id == user_id)
        user = self.session.exec(statement).one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Not Found")
        return User(self.session, user)  
        
    def get_one_by_username(self, username) -> User: 
        statement = select(UserDB).where(UserDB.username == username)
        user = self.session.exec(statement).one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Not Found")
        return User(self.session, user)  