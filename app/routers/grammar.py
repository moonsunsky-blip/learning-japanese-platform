from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session 

from typing import List, Optional

import app.crud as crud 
import app.models as models
import app.schemas as schemas 
from app.database import get_db

router = APIRouter(
    prefix = "/api/v1/grammar",
    tags = ["grammar"]
)

@router.get("/random", response_model = schemas.GrammarResponse)
def get_random_grammar_words(level: str = "N5", db: Session = Depends(get_db)):
    grammar_words = crud.get_random_grammar(db = db, level = level)
    if grammar_words is None:
        raise HTTPException(status_code = 404, detail = f"No grammar found for level {level}")
    return grammar_words

@router.get("/", response_model = List[schemas.GrammarResponse])
def get_grammar_title(
    grammar_title: Optional[str] = Query(None, alias = "title"),

    limit: int = Query(10, ge = 1, le = 100),
    offset: int = Query(0, ge = 0),

    db: Session = Depends(get_db)
):

    query = db.query(models.Grammar)

    if grammar_title:
        query = query.filter(models.Grammar.title.ilike(f"%{grammar_title}%"))

    grammar_items = query.offset(offset).limit(limit).all()
    return grammar_items