import sys
import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

# models.py'yi tanıyabilmek için sys.path ayarı
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Book, Library

def test_add_find_remove():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "lib.json")
        lib = Library(filepath)

        book = Book("Test Kitap", "Yazar", "123456")
        lib.add_book(book)
        assert lib.find_book("123456") is not None

        assert lib.remove_book("123456") is True
        assert lib.find_book("123456") is None

@patch("models.httpx.get")
def test_add_book_by_isbn(mock_get):
    # Open Library API yanıtı (kitap bilgisi)
    book_response = MagicMock()
    book_response.status_code = 200
    book_response.json.return_value = {
        "title": "Test Book",
        "authors": [{"key": "/authors/OL12345A"}]
    }

    # Yazar bilgisi yanıtı
    author_response = MagicMock()
    author_response.status_code = 200
    author_response.json.return_value = {
        "name": "Test Author"
    }

    # Sırasıyla 2 API çağrısına cevap vermesini sağla
    mock_get.side_effect = [book_response, author_response]

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "lib.json")
        lib = Library(filepath)

        added_book = lib.add_book_by_isbn("9781234567897")
        assert added_book.title == "Test Book"
        assert added_book.author == "Test Author"
        assert added_book.isbn == "9781234567897"
        assert lib.find_book("9781234567897") is not None
