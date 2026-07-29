from pydantic import BaseModel
from datetime import datetime

class BookBase(BaseModel):
    title: str
    description : str | None = None
    published_year : int 
    
    author_id : int
    category_id : int
    
    cover_image : str | None = None



class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    published_year: int | None = None
    author_id: int | None = None
    category_id: int | None = None
    cover_image: str | None = None

class BookInDBBase(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Book(BookInDBBase):
    pass
