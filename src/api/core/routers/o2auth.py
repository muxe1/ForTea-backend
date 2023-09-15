


from core.dependencies.db import get_session
from core.models.users import Token, UserCreate, UserLogin
from core.services import users
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, session: Session=Depends(get_session)) -> Token: 
    return users.register(user, session)  

@router.post("/login", response_model=Token)
def login(user: UserLogin, response: Response, session: Session=Depends(get_session)) -> Token:
    return users.login(user, response, session)

@router.post("/logout")
def logout(response: Response):
    return users.logout(response)




