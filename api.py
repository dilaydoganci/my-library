from fastapi import FastAPI, HTTPException
from models import Library
from schemas import ISBNRequest
import uvicorn

app = FastAPI()
library = Library()

@app.get("/")
def root():
    return {"message": "Library API is running!"}

@app.get("/books")
def list_books():
    return [vars(book) for book in library.list_books()]

@app.get("/books/{isbn}")
def get_book(isbn: str):
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return vars(book)

@app.post("/books")
def add_book(data: ISBNRequest):
    try:
        book = library.add_book_by_isbn(data.isbn)
        return vars(book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Bir hata oluştu.")

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    if not library.remove_book(isbn):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# Run with: uvicorn api:app --reload
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
