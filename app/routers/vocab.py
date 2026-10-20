from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session 

from typing import List, Optional

import app.crud as crud 
import app.schemas as schemas
import app.models as models
from app.database import get_db

router = APIRouter(
    prefix = "/api/v1/vocab",
    tags = ["vocab"]
)

@router.get("/", response_model = List[schemas.VocabResponse])
def get_vocabulary_list(
    vocab_type: Optional[str] = Query(None, alias = "type", description = "фильтр по типу слова (noun, verb итд)"),

    limit: int = Query(10, ge = 1, le = 100, description = "фильтр по кол слов на странице"),
    offset: int = Query(0, ge = 0, description = "сколько слов пропустить от начало"),

    db: Session = Depends(get_db)
):

    query = db.query(models.Vocab)

    if vocab_type:
        query = query.filter(models.Vocab.type == vocab_type)

    vocabulary_items = query.offset(offset).limit(limit).all()
    return vocabulary_items