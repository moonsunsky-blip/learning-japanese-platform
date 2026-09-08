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

@router.post("/alphabet/{item_id}", response_model = schemas.UserResponse)
def progress_creat_alphabet(item_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Alphabet, item_id = item_id, relation_name = "learned_alphabet")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress

@router.post("/kanji/{item_id}", response_model = schemas.UserResponse)
def progress_creat_kanji(item_id: int ,current_user: models.User = Depends(get_current_user) ,db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Kanji, item_id = item_id, relation_name = "learned_kanji")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress

@router.post("/vocab/{item_id}", response_model = schemas.UserResponse)
def progress_creat_vocab(item_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Vocab, item_id = item_id, relation_name = "learned_vocab")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress

@router.post("/grammar/{item_id}", response_model = schemas.UserResponse)
def progress_creat_grammar(item_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_progress = crud.user_progress(db = db, user_email = current_user.email, item_model = models.Grammar, item_id = item_id, relation_name = "learned_grammar")

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = "not found"
        )

    return user_progress 

CATEGORY_MAP = {
    "alphabet": (models.Alphabet, "learned_alphabet"),
    "kanji": (models.Kanji, "learned_kanji"),
    "vocab": (models.Vocab, "learned_vocab"),
    "grammar": (models.Grammar, "learned_grammar")
}


@router.post("/{category}/{item_id}", response_model = schemas.UserResponse)
def add_generic_progress(
    category: str,
    item_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if category not in CATEGORY_MAP:
        raise HTTPException(
            status_code = 400,
            detail = f"Invaild category. Allowed: {list(CATEGORY_MAP.keys())}"
        )

    item_model, relation_name = CATEGORY_MAP[category]

    user_progress = crud.user_progress(
        db = db,
        user_email = current_user.email,
        item_model = item_model,
        item_id = item_id,
        relation_name = relation_name
    )

    if user_progress is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with id: {item_id}, in category: {category} not found"
        )

    return user_progress

