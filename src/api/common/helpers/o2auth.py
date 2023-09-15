from os import environ
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=122)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, environ.get("SECRET_KEY"), environ.get("ALGORITHM"))
    return encoded_jwt

def decode(token: str):
    return jwt.decode(str(token), environ.get("SECRET_KEY"), algorithms=[environ.get("ALGORITHM")])