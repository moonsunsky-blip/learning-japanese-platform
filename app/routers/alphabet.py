from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session 

from typing import List, Optional

import app.models as models
import app.crud as crud
import app.schemas as schemas 
from app.database import get_db

router = APIRouter(
    prefix = "/api/v1/alphabet",
    tags = ["alphabet"]
)


@router.get("/random", response_model = schemas.AlphabetResponse)
def get_random_alphabet(alphabet_type: str, db: Session = Depends(get_db)):
    item = crud.get_random_alphabet(db = db, alphabet_type = alphabet_type)
    if item is None:
        raise HTTPException(status_code = 404, detail = f"no any alph. found for type {alphabet_type}")
    return item

"""
    здесь учитывается тип словаря 
    хирагана/катакана 
     
"""

@router.get("/", response_model = List[schemas.AlphabetResponse])
def get_alphabet_character_type(
    alphabet_type: Optional[str] = Query(None, alias = "type", description = "фильтрация типов"),
    russian: Optional[str] = Query(None, alias = "russian"),

    limit: int = Query(10, ge = 1, le = 100),
    offset: int = Query(0, ge = 0),

    db: Session = Depends(get_db)
):
    query = db.query(models.Alphabet)

    if alphabet_type:
        query = query.filter(models.Alphabet.type == alphabet_type)

    if russian:
        query = query.filter( models.Alphabet.russian.ilike(f"%{russian}%"))

    alphabet_items = query.offset(offset).limit(limit).all()
    return alphabet_items