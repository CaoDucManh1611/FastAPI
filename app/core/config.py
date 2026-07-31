import os

from pydantic import BaseModel


class Settings(BaseModel):
    project_name: str = "Book Management API"
    sqlalchemy_database_url: str = "postgresql://postgres:123456@localhost:5432/Data_Book"

settings = Settings()
