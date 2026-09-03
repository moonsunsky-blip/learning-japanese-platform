from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

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