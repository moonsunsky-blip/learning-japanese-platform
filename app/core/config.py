from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import ValidationError

class Settings(BaseSettings):
    
        SECRET_KEY: str
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        DATABASE_URL: str = "sqlite:///./data/japanese.db"

        model_config = SettingsConfigDict(
            env_file = ".env", env_file_encoding = "utf-8"
        )
    


try:
    settings = Settings()
except ValidationError as exc:
      print(exc)
      print(repr(exc.errors()[0]['type']))