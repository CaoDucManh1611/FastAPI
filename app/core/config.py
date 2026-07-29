from pydantic import BaseModel

class Settings(BaseModel):
    project_name: str = "Book Management API"
    sqlalchemy_database_url: str = "sqlite:///./app.db"
    
settings = Settings()
