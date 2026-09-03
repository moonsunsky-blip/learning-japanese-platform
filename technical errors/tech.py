from sqlalchemy.orm import session
from app.database import SessionLocal
import app.models as models
from sqlalchemy import  inspect

db = SessionLocal()

for mapper in models.Base.registry.mappers:
    model_class = mapper.class_
    table_name = model_class.__tablename__

    total  = db.query(model_class).count()
    print(f"\n=== {table_name} ({model_class.__name__}) ===")
    print(f"всего записей : {total}")

    if total == 0:
        continue

    columns = [c for c in model_class.__table__.columns if c.name != "id"]

    from sqlalchemy import func
    duplicates = (
        db.query(*columns, func.count(model_class.id).label("count"))
        .group_by(*columns)
        .having(func.count(model_class.id) > 1)
        .all()
    )

    if duplicates:
        print(f"найдено {len(duplicates)} групп дублей!")
        for d in duplicates[:5]:
            print(f"  count = {d.count} | {dict(zip([c.name for c in columns], d[:-1]))}")
        else:
            print("дубли не найдены")

db.close()

import os

data_dir = "data"
files_to_check = ["kanji.txt", "grammar_n5.txt", "N5_words.txt", "katakana.txt", "hiragana.txt"]

for fname in files_to_check:
    path = os.path.join(data_dir, fname)
    if os.path.exists(path):
        with open(path, "r", encoding = "utf-8")as f:
            lines = sum(1 for line in f if line.strip() and not line.startswith("#"))
        print(f"{fname}: {lines} строк")

    else:
        print(f"{fname}: файл не найден ")