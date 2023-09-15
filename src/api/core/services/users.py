from core.models.users import (Token, UserAPI, UserCreate, UserDB, UserLogin,
                               UserPosts, UserUpdate)
from core.utils.users import User, Users
from fastapi import Response, Request
from sqlmodel import Session

    
def register(user: UserCreate, session: Session) -> Token:
    return User(session, user).create().register()

def login(user: UserLogin, response: Response, session: Session) -> Token:
    return User(session, user).login(response)

def logout(response: Response):
    return User.logout(response)
    
def get_by_session(request: Request, session: Session) -> UserAPI:
    return Users(session).get_by_session(request)

def get(user_id: int, session: Session) -> UserAPI: 
    user = Users(session).get(user_id)
    return user.to_api()

def get_by_username(username: str, session: Session) -> UserAPI: 
    user = Users(session).get_one_by_username(username)
    return user.to_api()

def update(current_user: UserDB, user_data_for_update: UserUpdate, session: Session) -> UserAPI:
    user = User(session, current_user).update(user_data_for_update)
    return user.to_api()

def update_photo(photo_id: int, user: UserDB, session: Session) -> UserAPI:
    _user = User(session, user).update_photo(photo_id)
    return _user.to_api()

def get_all_posts(user_id: str, session: Session, offset: int, limit: int) -> UserPosts:
    user_posts = Users(session).get(user_id).get_all_posts(offset, limit)
    return UserPosts(user_id=user_id, posts=[i.post_id for i in user_posts])
