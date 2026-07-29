from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_authors():
    return {"message": "List of authors do it latter"}