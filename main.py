import os
import random
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func 

from app import models
from app.database import engine, SessionLocal

from app.database import SessionLocal
import app.models as models
import app.crud as crud

app = FastAPI()

templates = Jinja2Templates(directory = "templates")
templates.env.cache = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_random(db: Session):
    return db.query(models.Vocab).order_by(func.random()).first()

def get_random_letter(db: Session):
    return db.query(models.Alphabet).order_by(func.random()).first()


def get_test_for_begin(db: Session, correct_word):

    notcor_word = db.query(models.Vocab).filter(models.Vocab.id != correct_word.id).order_by(func.random()).limit(3).all()
    
    
    option = [correct_word] + notcor_word
    random.shuffle(option)
    
    return option 


@app.get("/", response_class = HTMLResponse)
async def home(db: Session = Depends(get_db)):

    current_word = get_random(db)

    if current_word is not None:
        word_text = current_word.words
        romaji = current_word.romaji
        russian = current_word.russian
        vocab_type = current_word.type
    else:
        word_text = "ошибка"
        russian = "база данных пуста, запустите db_init.py"
        romaji = "-"
        vocab_type = "-"

    return f"""
    <html>
        <head>
            <title>japanLNG</title>
        </head>
        <body style="text-align: center; font-family: Arial; margin-top: 100px;">
            <h1>🇯🇵 Слово дня 🇯🇵</h1>
            <div style="font-size: 48px; font-weight: bold; color: #2c3e50;">
                {word_text}
            </div>
            <h2 style="color: #7f8c8d; font-weight: normal; margin-top: 20px;">
                Перевод: {russian}
            </h2>
            <h3 style="color: #297bbc; font-weight: normal; margin-top: 20px;">
                произношение: {romaji}
            </h3>
            <h4 style="color: #3397e6; font-weight: normal; margin-top: 20px;">
                тип азбуки: {vocab_type}
            </h4>
            <p style="margin-top: 50px; color: #bdc3c7;">Обнови страницу (F5), чтобы увидеть новое слово!</p>
            <p style="margin-top: 30px;">
                <a href="/alphabet" style="color: #297bbc; text-decoration: none; font-size: 18px; font-weight: bold;">
                    Перейти к изучению азбуки →
                </a>
            </p>
        </body>
    </html>
    """



@app.get("/alphabet", response_class = HTMLResponse)
async def alphabet_page(db: Session = Depends(get_db)):

    
    current_letter = get_random_letter(db)

    if current_letter is not None:
        letter_text = current_letter.character
        romaji = current_letter.romaji
        russian = current_letter.russian
        abc_type = current_letter.type
    else:
        letter_text = "Ошибка"
        russian = "База данных пуста"
        romaji = "-"
        abc_type = "-"

    return f"""
    <html>
        <head>
             <title>japanLNG</title>
        </head>
        <body style="text-align: center; font-family: Arial; margin-top: 100px;">
            <h1>🇯🇵 Буква дня 🇯🇵</h1>
            <div style="font-size: 48px; font-weight: bold; color: #2c3e50;">
                {letter_text}
            </div>
            <h2 style="color: #7f8c8d; font-weight: normal; margin-top: 20px;">
                Перевод: {russian}
            </h2>
            <h3 style="color: #297bbc; font-weight: normal; margin-top: 20px;">
                произношение: {romaji}
            </h3>
            <h4 style="color: #3397e6; font-weight: normal; margin-top: 20px;">
                тип азбуки: {abc_type}
            </h4>
            <p style="margin-top: 50px; color: #bdc3c7;">Обнови страницу (F5), чтобы увидеть новое слово!</p>
            <p style="margin-top: 30px;">
                <a href="/" style="color: #2c3e50; text-decoration: none; font-size: 18px; font-weight: bold;">
                    ← Перейти к словарному запасу N5
                 </a>
            </p>
            <!-- НОВАЯ ССЫЛКА НА ТЕСТ -->
            <p style="margin-top: 15px;">
                <a href="/test" style="color: #27ae60; text-decoration: none; font-size: 18px; font-weight: bold;">
                    🧠 Пройти тест по словам →
                </a>
            </p>
        </body>
    </html>
    """

@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request, db: Session = Depends(get_db)):
    correct_word = db.query(models.Vocab).order_by(func.random()).first()
    option = get_test_for_begin(db, correct_word)

    return templates.TemplateResponse(
        request=request,
        name="test.html",
        context={"correct_word": correct_word, "options": option}
    )


