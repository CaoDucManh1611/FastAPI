from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from app.api.deps import get_db
from app import models
from app.schemas.category import Category, CategoryCreate, CategoryUpdate


router = APIRouter()
#Get all category
@router.get("/", response_model=list[Category])
def list_categories(
    db: Session = Depends(get_db)
):
    categories = db.query(models.Category).all()
    return categories

#Get category_id
@router.get("/{category_id}", response_model=Category)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


#Create category
@router.post("/", response_model=Category, status_code= status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db)
):
    if db.query(models.Category).filter(models.Category.name == category_in.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")

    category = models.Category(name=category_in.name, description=category_in.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


#Update category
@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    if not db.query(models.Category).filter(models.Category.id == category_id).first():
        raise HTTPException(status_code=404, detail="Category not found")
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category_update.name == category.name:
        raise HTTPException(status_code=400, detail="No changes detected because the name is the same")
    category.name = category_update.name
    category.description = category_update.description
    db.commit()
    db.refresh(category)
    return category

#Delete category
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return None