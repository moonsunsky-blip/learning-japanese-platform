# === импорты ===

from sqlalchemy.orm import Session 
from app import models 
from sqlalchemy import func
from app import schemas



# =====================================================
# =====================================================


# ============================ иероглифы ============================

def get_random_alphabet(db: Session, alphabet_type: str):
    """рандом """
    return db.query(models.Alphabet).filter(models.Alphabet.type == alphabet_type).order_by(func.random()).first()

def get_all_alphabet_by_type(db: Session, alphabet_type: str, skip: int = 0, limit = 50):
    return db.query(models.Alphabet).filter(models.Alphabet.type == alphabet_type).offset(skip).limit(limit).all()

def get_alphabet_by_hiragana(db: Session, translation,  alphabet_type: str = "hiragana"):
    return db.query(models.Alphabet).filter(models.Alphabet.type == alphabet_type, models.Alphabet.russian == translation).first()

def get_alphabet_by_katakana(db: Session, translation, alphabet_type: str = "katakana"):
    return db.query(models.Alphabet).filter(models.Alphabet.type == alphabet_type, models.Alphabet.russian == translation).first()

# ==========================================================




# ============================= кандзи ================================ 

def get_kanji_by_id(db: Session, kanji_id: int):
    """получить один кандзи по его ID"""
    return db.query(models.Kanji).filter(models.Kanji.id == kanji_id).first()

def get_kanji_by_character(db: Session, character: str):
    """Найти кандзи по самому иероглифу (например, '日')"""
    return db.query(models.Kanji).filter(models.Kanji.character == character).first()

def get_random_kanji(db: Session, level: str):
    """ получить рандом кандзи"""
    return db.query(models.Kanji).filter(models.Kanji.level == level).order_by(func.random()).first()

def get_all_by_kanji(db: Session, skip: int = 0, limit: int = 100):
    """получить список кандзи с пагинацией"""
    return db.query(models.Kanji).offset(skip).limit(limit).all()

def get_kanji_by_jlpt(db: Session, level: str):
    """получить список кандзи по уронвю JLPT (например 'N5')"""
    return db.query(models.Kanji).filter(models.Kanji.level == level).all()

# ===========================================================================



# ======================= грамматика ===========================

def get_grammar_by_category(db: Session, category, level: str):
    return db.query(models.Grammar).filter(models.Grammar.category == category, models.Grammar.level == level).all()

def get_random_grammar(db:Session, level: str):
    return db.query(models.Grammar).filter(models.Grammar.level == level).order_by(func.random()).first()

def get_all_grammar(db: Session, skip: int, limit: int = 50):
    return db.query(models.Grammar).offset(skip).limit(limit).all()

def get_grammar_by_meaning(db: Session, meaning: str):
    return db.query(models.Grammar).filter(models.Grammar.meaning == meaning).first()
# ==============================================================
 
# ======================= словарный запас ======================

def get_vocab_by_level(db: Session, level):
    return db.query (models.Vocab).filter(models.Vocab.type == level).first()

def get_all_vocab_by_level(db: Session, level):
    return db.query (models.Vocab).filter(models.Vocab.type == level).all()

def get_vocab_by_random(db: Session, level):
    return db.query (models.Vocab).filter(models.Vocab.type == level).order_by(func.random()).first()

def get_vocab_by_meaning(db: Session, russian):
    return db.query (models.Vocab).filter(models.Vocab.russian == russian).first()


# ========================================================================
# ========================================================================


# ================================ создание данных =======================

def create_kanji(db: Session, kanji: str, readings: str, meaning: str, jlpt: str = None):
    db_kanji = models.Kanji(
        kanji = kanji,
        readings = readings,
        meaning = meaning,
        jlpt = jlpt
    )
    db.add(db_kanji)
    db.commit()
    db.refresh(db_kanji)
    return db_kanji

# =================================================================
# =================================================================


# =========================================================================
# =================================== удаление данных =====================

def delete_kanji(db:Session, kanji_id: int):
    """удалить данные кандзи по ID"""
    db_kanji = get_kanji_by_id(db, kanji_id)
    if db_kanji:
        db.delete(db_kanji)
        db.commit()
        return True
    return False

# ================================================================
# ================================================================




# =======================================================
# ПОЛЬЗОВАТЕЛИ 
# =======================================================

def get_user_by_email(db: Session, email: str):
    return db.query (models.User).filter(models.User.email == email).first()

def get_user(db:Session, email: str):
    return db.query (models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """ СОЗДАНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ С ХЭШИРОВАННЫМ ПАРОЛЕМ"""

    db_user = models.User(
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ======================================================

# ======================================================




# ======================================================
# ============== ЛОГИКА ВЫДАЧА КОНТНЕТА ================
# ======================================================

def get_filter_by_level(db: Session, model, level: str):
    """ пользователь вводит тип каталога и его уровень """
    return db.query(model).filter(model.level == level).all()

# ===

def progress_of_kanji_user(db: Session, learn_element, user_email):
    user = db.query (models.User).filter(models.User.email == user_email).first()
    kanji = db.query (models.Kanji).filter(models.Kanji.id == learn_element).first()  

    if not user or not kanji:
        return None
    
    if kanji not in user.learned_kanji:
        user.learned_kanji.append(kanji)
        db.commit()
        db.refresh(user)
    

    return user
    
# === 
# ===

def user_progress(db: Session, user_email, item_model, item_id, relation_name):
    user = db.query (models.User).filter(models.User.email == user_email).first()
    model = db.query (item_model).filter(item_model.id == item_id).first()
    
    if not user or not model:
        return None
    
    user_list = getattr(user, relation_name)
    
    if model not in user_list:
        user_list.append(model)
        db.commit()
        db.refresh(user)

    return user
# ===
def get_user_progress(db: Session, user_email: str, relation_name: str):
    user = db.query (models.User).filter(models.User.email == user_email).first()

    if not user:
        return None

    return getattr(user, relation_name)

