import sys
sys.path.insert(0, r"c:\Users\PC\Software\app")

import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy.orm import Session
from app.database import  SessionLocal
import app.models as models 
import app.crud as crud


db = SessionLocal()

all_grammar = db.query(models.Grammar).all()

print(f"всего записей в таблице grammar: {len(all_grammar)}")

for g in all_grammar[:10]:
    print(f"id = {g.id} | category = {g.category} | level = {g.level}")