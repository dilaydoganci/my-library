import sys
import os
import pytest
from fastapi.testclient import TestClient

# api.py'deki FastAPI instance'ını import et
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api import app

client = TestClient(app)

def test_get_books_initially_empty():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_and_delete_book(monkeypatch):
    test_isbn = "9780140328721"

    # OpenLibrary API çağrılarını mock'la
    class MockResponse:
        def __init__(self, json_data, status_code):
            self._json = json_data
            self.status_code = status_code

        def json(self):
            return self._json

    def mock_get(url, timeout=10.0):
        if "isbn" in url:
            return MockResponse({
                "title": "Mock Book",
                "authors": [{"key": "/authors/OL12345A"}]
            }, 200)
        elif "/authors/OL12345A" in url:
            return MockResponse({
                "name": "Mock Author"
            }, 200)
        return MockResponse({}, 404)

    monkeypatch.setattr("models.httpx.get", mock_get)

    # POST /books
    post_response = client.post("/books", json={"isbn": test_isbn})
    assert post_response.status_code == 200
    assert post_response.json()["isbn"] == test_isbn

    # GET /books
    get_response = client.get("/books")
    assert get_response.status_code == 200
    assert any(book["isbn"] == test_isbn for book in get_response.json())

    # DELETE /books/{isbn}
    delete_response = client.delete(f"/books/{test_isbn}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Kitap silindi."
