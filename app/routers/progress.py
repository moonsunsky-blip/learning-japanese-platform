from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.models as models
import app.crud as crud
import app.schemas as schemas
from app.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix = "/api/v1/progress",
    tags = ["Progress"]
)

@router.post("/progress/alphabet/{item_id}", response_model = schemas.UserResponse)
def progress_creat_alphabet(item_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Alphabet, item_id = item_id, relation_name = "learned_alphabet")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress

@router.post("/progress/kanji/{item_id}", response_model = schemas.UserResponse)
def progress_creat_kanji(item_id: int ,current_user: models.User = Depends(get_current_user) ,db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Kanji, item_id = item_id, relation_name = "learned_kanji")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress

@router.post("/progress/vocab/{item_id}", response_model = schemas.UserResponse)
def progress_creat_vocab(item_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Vocab, item_id = item_id, relation_name = "learned_vocab")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress

@router.post("/progress/grammar/{item_id}", response_model = schemas.UserResponse)
def progress_creat_grammar(item_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Grammar, item_id = item_id, relation_name = "learned_grammar")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress 