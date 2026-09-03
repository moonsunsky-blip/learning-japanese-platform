import os
from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db

from app.core.config import settings

from app.database import Base, engine
import app.models

from app.routers import kanji
from app.routers import grammar
from app.routers import alphabet
from app.routers import auth




app = FastAPI(title = "WaGo")

app.include_router(kanji.router)

app.include_router(grammar.router)

app.include_router(alphabet.router)

app.include_router(auth.router)

