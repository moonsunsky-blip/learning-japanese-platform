from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from typing import List, Optional

import app.crud as crud
import app.models as models
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

@router.get("/", response_model = List[schemas.KanjiResponse])
def get_kanji_list(
    kanji_meaning: Optional[str] = Query(None, alias = "meaning", description = "фильтр слов"),

    limit: int = Query(10, ge=1, le = 100, description = "кол слов на стр"),
    offset: int = Query(0, ge =0, description = "пропуск слов от начало"),

    db: Session = Depends(get_db)
):

    query = db.query(models.Kanji)

    if kanji_meaning:
        query = query.filter(models.Kanji.meaning.ilike(f"%{kanji_meaning}%"))

    kanji_items = query.offset(offset).limit(limit).all()
    return kanji_items