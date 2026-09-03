from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

import app.crud as crud 
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

