import os
from app.database import engine, SessionLocal
import app.models as models
from sqlalchemy.orm import Session

from app import models
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind = engine)

db = SessionLocal()

def pirsing(file_read):
    read_list = []

    with open(file_read, "r", encoding = "utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue
            parts = [p.strip() for p in line.split("|")]

            if len(parts) == 4:
                kanji_obj = models.Kanji(
                    character = parts[0],
                    onyomi=parts[1],
                    kunyomi=parts[2],
                    meaning=parts[3]
                )
                read_list.append(kanji_obj)

    return read_list


def seed_kanji():
    db = SessionLocal()

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data", "kanji.txt")
        kanji_list = pirsing(file_path)

        db.add_all(kanji_list)
        db.commit()
        print(f"успешно добавлено {len(kanji_list)} в базу")

    except Exception as e:
        db.rollback()
        print(f"ошибка при заполнении базы: {e}")

    finally:
        db.close()
# ======================================================================


def seed_from_file(db:Session, file_path: str, model_class, field_names: list[str], extra_fields: dict = None):
    existing_count = db.query(model_class).count()
    if existing_count > 0:
        print(f"в таблице {model_class.__tablename__} уже есть {existing_count} записей, пропускаем сидинг")
        return
    objects = []

    with open(file_path, "r", encoding = "utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]

            if len(parts) == len(field_names):
                data_dict = dict(zip(field_names, parts))
                if extra_fields:
                    data_dict.update(extra_fields)

                obj = model_class(**data_dict)
                objects.append(obj)
            else:
                print(f"пропущена строка (ожидалось {len(field_names)}) : получено {len(parts)} : {line[:50]} ...")

    if objects:
        db.add_all(objects)
        db.commit()
        print(f"Успешно загружено {len(objects)} записей для {model_class.__tablename__}")
    else:
        print(f"НИЧЕГО НЕ ДОБАВЛЕНО {model_class.__tablename__} - проверьте формат файла {file_path}")

MAPPINGS = [
    (
        "grammar_n5.txt",
        models.Grammar,
        ["title", "category", "structure", "meaning", "explanation"], {"level": "N5"}
    )
]

def run_seed():
    db = SessionLocal()
    current_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        for file_name, model_class, field_names, extra_fields in MAPPINGS:
            file_path = os.path.join(current_dir, "data", file_name)

            if os.path.exists(file_path):
                seed_from_file(
                    db=db,
                    file_path = file_path,
                    model_class = model_class,
                    field_names = field_names,
                    extra_fields = extra_fields
                )
            else:
                print(f" Файл {file_name} не найден, пропускаем")

        print("база данных успешно заполнена")

    except Exception as e:
        db.rollback()
        print(f"ошибка при заполнении: {e}")
    finally:
        db.close()
    
if __name__ == "__main__":
    run_seed()

    db = SessionLocal()
    count = db.query(models.Grammar).count()
    print(f"Проверка: сейчас в таблице grammar {count} записей")
    db.close()
           