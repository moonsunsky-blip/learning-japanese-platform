from  pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class AlphabetResponse(BaseModel):
    id: int
    character: str
    romaji: str
    russian: str
    type: str

    model_config = ConfigDict(from_attributes = True)

class VocabResponse(BaseModel):

    id: int
    words: str
    romaji: str
    russian: str
    type: str 

    model_config = ConfigDict(from_attributes = True)

class KanjiResponse(BaseModel):

    id: int
    character: str
    onyomi: str
    kunyomi: str
    meaning: str
    level: str

    model_config = ConfigDict(from_attributes = True)


class GrammarResponse(BaseModel):

    id: int
    title: str
    category: str
    structure: str
    meaning: str
    explanation: str
    level: str

    model_config = ConfigDict(from_attributes = True)

class UserCreate(BaseModel):

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_premium: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
        