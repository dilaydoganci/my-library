import json
import os
import httpx  # Harici API çağrısı için

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class Library:
    def __init__(self, storage_file: str = "library.json"):
        self.storage_file = storage_file
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.books = [Book(**item) for item in data]
            except json.JSONDecodeError:
                self.books = []
        else:
            self.books = []

    def save_books(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump([vars(b) for b in self.books], f, ensure_ascii=False, indent=2)

    def add_book(self, book: Book):
        if self.find_book(book.isbn):
            raise ValueError("Bu ISBN zaten kayıtlı.")
        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn: str):
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def list_books(self):
        return self.books

    def find_book(self, isbn: str):
        return next((b for b in self.books if b.isbn == isbn), None)

    def add_book_by_isbn(self, isbn: str):
        print(f"🔎 API sorgulanıyor: {isbn}")
        if self.find_book(isbn):
            raise ValueError("Bu ISBN zaten kayıtlı.")

        url = f"https://openlibrary.org/isbn/{isbn}.json"

        try:
            response = httpx.get(url, timeout=10.0, follow_redirects=True)

            print(f"🌐 Yanıt geldi. Status code: {response.status_code}")

            if response.status_code == 404:
                raise LookupError("Kitap bulunamadı.")
            elif response.status_code != 200:
                raise ConnectionError(f"API hatası: {response.status_code}")

            try:
                data = response.json()
                print("📦 JSON çözüldü.")
            except Exception as e:
                print("⚠️ JSON parse hatası. Gelen içerik:")
                print(response.text)
                raise e

            title = data.get("title", "Bilinmeyen Başlık")

            # Yazar bilgisi
            authors = data.get("authors", [])
            author_names = []
            for a in authors:
                key = a.get("key")
                if key:
                    try:
                        print(f"🔗 Yazar verisi çekiliyor: {key}")
                        auth_resp = httpx.get(f"https://openlibrary.org{key}.json", timeout=10.0)
                        if auth_resp.status_code == 200:
                            name = auth_resp.json().get("name")
                            if name:
                                author_names.append(name)
                    except Exception as e:
                        print(f"❌ Yazar verisi alınamadı: {e}")

            author = ", ".join(author_names) if author_names else "Bilinmeyen Yazar"

            book = Book(title=title, author=author, isbn=isbn)
            self.books.append(book)
            self.save_books()
            print("✅ Kitap başarıyla eklendi.")
            return book

        except httpx.RequestError as e:
            print("❌ RequestError oluştu:", e)
            raise ConnectionError("API'ye erişilemedi (RequestError).") from e
        except Exception as e:
            print("❌ Genel hata:", e)
            raise
