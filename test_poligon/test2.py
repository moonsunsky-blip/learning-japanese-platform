import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import app.models as models  
from app import models
from app.database import engine, SessionLocal

base = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(base, "data", "japanese.db")
fix_db = os.path.abspath(db_file).replace('\\', '/')

URL = f"sqlite:///{fix_db}"

engine = create_engine(URL, echo=True)


with Session(bind=engine) as session:
    
    first_kanji = session.query(models.Kanji).first()
    
    if first_kanji:
        print("\n--- УСПЕХ! Первичная запись найдена ---")
        print(f"Иероглиф: {first_kanji.character} | Значение: {first_kanji.meaning}")
    else:
        print("\n--- База пуста или таблица не найдена ---")


# не забудь вытащить файл из папки и поставить их рядом с другими py файлами