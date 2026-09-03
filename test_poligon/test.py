import os
from app import models
from app.database import engine, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Request
from sqlalchemy import func
import app.models as models 

from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_word(db: Session):
    word = db.query(models.Kanji).filter(models.Kanji.meaning == "мужчина").first() 
    special_word = db.query(models.Kanji).filter(models.Kanji.meaning.contains("вода")).all()
    all_words = db.query(models.Kanji).order_by(func.random()).limit(3).all()

    return word, special_word, all_words



if __name__ == "__main__":
    db = SessionLocal()
    try:
        single_kanji, water_kanjis, random_kanjis = get_word(db)

        print("\n=== 1. ПОИСК... ===")
        if single_kanji:
            print(f"найден : {single_kanji.character} [{single_kanji.onyomi} / {single_kanji.kunyomi}] - {single_kanji.meaning}")
        else:
            print("ничего не найдено")

        print("\n === 2. ПОИСК ПО ПОДСТРОКЕ ('вода') ===")
        print(f"найдено совпадений : {len(water_kanjis)}")
        for i in water_kanjis:
                print(f"- {i.character}: {i.meaning}")

        print("\n=== 3. СЛУЧАЙНЫЕ 3 КАНДЗИ ===")
        for k in random_kanjis:
            print(f"- {k.character} ({k.character})")
    finally:
        db.close()

def my_count(db: Session):
    total_count = db.query(models.Kanji).count()
    water_count = db.query(models.Kanji).filter(models.Kanji.meaning.contains("вода")).count()

    return total_count, water_count

def update_kanji(db: Session, character: str, new_meaning: str):
    kanji = db.query(models.Kanji).filter(models.Kanji.character == character).first()

    if kanji:
        kanji.meaning = new_meaning
        db.commit()
        db.refresh(kanji)
        return kanji
    return None

def delete_kanji(db: Session, character = str):
    kanji = db.query(models.Kanji).filter(models.Kanji.character == character).first()
    if kanji:
        db.delete(kanji)
        db.commit()
        return True
    return False

