from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

import app.crud as crud 
import app.schemas as schemas
from app.database import get_db

router = APIRouter(
    prefix = "/api/v1/vocab",
    tags = ["vocab"]
)

