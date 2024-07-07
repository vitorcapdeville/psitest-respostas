from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PSITEST_EMAILS: str
    FRONT_END_URL: str


@lru_cache
def get_settings():
    return Settings()
