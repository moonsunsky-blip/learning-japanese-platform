from app.database import SessionLocal
import app.models as models
from seed_db import seed_from_file
import os

db = SessionLocal()

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data", "grammar_n5.txt")

seed_from_file(
    db = db,
    file_path = file_path,
    model_class = models.Grammar,
    field_names = ["title", "category", "structure", "meaning", "explanation"],
    extra_fields = {"level": "N5"}
)
print("готово")
db.close()