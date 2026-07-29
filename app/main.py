from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import authors, books, categories
app = FastAPI(
    title="Book management API",
    description="This is a simple API for managing books in a library.",
    version="1.0.0"
)


app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book management API!"}