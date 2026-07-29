import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app import models
from app.schemas.book import Book, BookCreate, BookUpdate
from app.schemas.author import Author
from app.schemas.category import Category

router = APIRouter()



@router.get("/")
def get_books(
    db: Session = Depends(get_db)
):
    books = db.query(models.Book).all()
    return books

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db)
):
    author = db.query(models.Author).filter(models.Author.id == book_in.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    category = db.query(models.Category).filter(models.Category.id == book_in.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    book = models.Book(
        title=book_in.title,
        description=book_in.description,
        published_year=book_in.published_year,
        author_id=book_in.author_id,
        category_id=book_in.category_id,
        cover_image=book_in.cover_image
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book_update.title is not None:
        book.title = book_update.title
    if book_update.description is not None:
        book.description = book_update.description
    if book_update.published_year is not None:
        book.published_year = book_update.published_year
    if book_update.author_id is not None:
        author = db.query(models.Author).filter(models.Author.id == book_update.author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        book.author_id = book_update.author_id
    if book_update.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == book_update.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        book.category_id = book_update.category_id
    if book_update.cover_image is not None:
        book.cover_image = book_update.cover_image
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.put("/{book_id}/cover", response_model=Book, status_code=status.HTTP_200_OK)
def upload_book_cover(
    book_id: int,
    file:UploadFile = File(...),
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only image files are allowed.")

    upload_dir = Path("app/static/covers")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{book_id}_{file.filename}"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    book.cover_image = f"/static/covers/{book_id}_{file.filename}"

    db.commit()
    db.refresh(book)
    return book
