from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from app.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

# промежуточная таблица 

user_alphabet = Table(
    "user_alphabet",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key = True),
    Column("alphabet_id", Integer, ForeignKey("alphabet.id"), primary_key = True)
)

user_vocab = Table(
    "user_vocab",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key = True),
    Column("vocab_id", Integer, ForeignKey("vocabulary.id"), primary_key = True)
)

user_grammar = Table(
    "user_grammar",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key = True),
    Column("grammar_id", Integer, ForeignKey("grammar.id"), primary_key = True)
)


user_kanji = Table(
    "user_kanji",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key = True),
    Column("kanji_id", Integer, ForeignKey("kanji.id"), primary_key = True)
)

# ====================


# ======================================================

class Alphabet(Base):
    __tablename__ = "alphabet"

    id = Column(Integer, primary_key = True, autoincrement = True)
    character = Column(String, nullable = False)
    romaji = Column(String, nullable = False)
    russian = Column(String, nullable=  False)
    type = Column(String, nullable = False)

    users = relationship("User", secondary = user_alphabet, back_populates = "learned_alphabet")

class Vocab(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key = True, autoincrement = True)
    words = Column(String, nullable = False)
    romaji = Column(String, nullable = False)
    russian = Column(String, nullable = False)
    type = Column(String, nullable = False)

    users = relationship("User", secondary = user_vocab, back_populates = "learned_vocab")

class Kanji(Base):
    __tablename__ = "kanji"

    id = Column(Integer, primary_key = True, autoincrement = True)
    character = Column(String, nullable = False)
    onyomi = Column(String)
    kunyomi = Column(String)
    meaning = Column(String, nullable = False)
    level = Column(String, default = "N5")

    users = relationship("User", secondary = user_kanji, back_populates = "learned_kanji")
    
class Grammar(Base):
    __tablename__ = "grammar"

    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String, nullable = False)    # Название правила (например: "Частица は" или "Указательное местоимение これ")
    category = Column(String, nullable=False)    # Тип: "particles", "verbs", "adjectives", "demonstratives", "forms"
    structure = Column(String, nullable=False)   # Конструкция (например: "Существительное + は + Существительное + です")
    meaning = Column(String, nullable=False)     # Значение/перевод (например: "Являетсячем-то / Выделение темы")
    explanation = Column(Text, nullable=True)    # Подробное пояснение правила
    level = Column(String, default = "N5")

    users = relationship("User", secondary = user_grammar, back_populates = "learned_grammar")

# ===================================================================
    
# ============ Отдельный каталог моделей ДЛЯ ЛОИГНОВ     ============

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False)
    is_active = Column(Boolean, default = True)
    is_premium = Column(Boolean, default = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    learned_alphabet = relationship("Alphabet", secondary = user_alphabet, back_populates = "users")
    learned_vocab = relationship("Vocab", secondary = user_vocab, back_populates = "users")
    learned_kanji = relationship("Kanji",secondary = user_kanji, back_populates = "users")
    learned_grammar = relationship("Grammar", secondary = user_grammar, back_populates = "users")

# ===================================================
