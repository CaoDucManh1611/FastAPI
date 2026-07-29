from fastapi import APIRouter,HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from app.api.deps import get_db
from app import models
from app.schemas.author import Author, AuthorCreate, AuthorUpdate


router = APIRouter()


@router.get("/", response_model=list[Author], status_code=status.HTTP_200_OK)
def get_authors(
    db: Session = Depends(get_db)
):
    authors = db.query(models.Author).all()
    return authors

@router.get("/{author_id}", response_model=Author, status_code=status.HTTP_200_OK)
def get_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(
    author_in: AuthorCreate,
    db: Session = Depends(get_db)
):
    author = models.Author(name=author_in.name, bio=author_in.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

@router.put("/{author_id}", response_model=Author, status_code=status.HTTP_200_OK)
def update_author(
    author_id: int,
    author_update: AuthorUpdate,
    db: Session = Depends(get_db)
):
    if not db.query(models.Author).filter(models.Author.id == author_id).first():
        raise HTTPException(status_code=404, detail="Author not found")
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author_update.name is not None:
        author.name = author_update.name
    if author_update.bio is not None:
        author.bio = author_update.bio
    db.commit()
    db.refresh(author)
    return author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    if not db.query(models.Author).filter(models.Author.id == author_id).first():
        raise HTTPException(status_code=404, detail="Author not found")
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    db.delete(author)
    db.commit()
    return None
