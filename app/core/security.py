from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.core.config import settings

import bcrypt
import app.crud as crud
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext
from app.database import get_db

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/v1/auth/login")



def hash_password(password: str) -> str:
    """хэш пароль пользователя"""
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """проверка с совпадением пароли с хэшем из базы"""
    pwd_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
    return encode_jwt

def get_current_user(
        token: str = Depends(oauth_2_scheme), db: Session = Depends(get_db)
        ):
    credentials_excpetion = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])          # 1. Расшифровываем JWT токен
                                                                                

        email: str = payload.get("sub")                                            # 2. Достаем email из поля "sub"
        if email is None:                                                          # 3. Находим пользователя в БД
            raise credentials_excpetion                                            # 4. Если токен протух или поддельный — выдаем 401 Unauthorized
    except PyJWTError:
        raise credentials_excpetion
    user = crud.get_user_by_email(db = db, email = email)
    if user is None:
        raise credentials_excpetion
    return user 


