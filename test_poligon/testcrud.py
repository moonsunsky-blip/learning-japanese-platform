from app.database import SessionLocal 
import app.models as models 
import app.crud as crud

db = SessionLocal()


word_kanji = crud.get_kanji_by_id(db, 5)

if word_kanji:
    print(word_kanji.__dict__)
else:
    print("не найден")

all_kanji = crud.get_all_by_kanji(db, limit=5)
print(f"Всего получено: {len(all_kanji)} кандзи")

db.close()