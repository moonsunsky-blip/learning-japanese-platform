from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas 
from app.database import get_db

router = APIRouter(
    prefix = "/api/v1/kanji",
    tags = ["kanji"]
)

@router.get("/random", response_model = schemas.KanjiResponse)
def get_random_kanji(level: str = "N5", db: Session = Depends(get_db)):
    kanji_item = crud.get_random_kanji(db = db, level = level)
    if kanji_item is None:
        raise HTTPException(status_code = 404, detail = f"no kanji found for level {level}")
    return kanji_item
