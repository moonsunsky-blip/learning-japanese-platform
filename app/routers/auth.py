from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 

import app.crud as crud 
import app.schemas as schemas 
from app.core.security import hash_password, verify_password, create_access_token
from app.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix = "/api/v1/auth",
    tags = ["Auth"]
)

@router.post("/register", response_model = schemas.UserResponse, status_code = status.HTTP_201_CREATED)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, email = user_data.email)
    if db_user:
        raise HTTPException(
            status_code = 400, 
            detail = "User with this email already exists"
        )

    hashed_pwd = hash_password(user_data.password)

    return crud.create_user(db = db, user = user_data, hashed_password = hashed_pwd)

@router.post("/login", response_model = schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email = form_data.username)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(data = {"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model = schemas.UserResponse)
def get_user_now(current_user = Depends(get_current_user)):
    return current_user