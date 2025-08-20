import sys
from models import Library

def print_usage():
    print("""
Kullanım:
  python main.py add <ISBN>
  python main.py remove <ISBN>
  python main.py find <ISBN>
  python main.py list
""")

def main():
    lib = Library()
    args = sys.argv[1:]

    if not args:
        print_usage()
        return

    cmd = args[0]

    if cmd == "add":
        if len(args) != 2:
            print("Kullanım: python main.py add <ISBN>")
            return
        isbn = args[1]
        try:
            book = lib.add_book_by_isbn(isbn)
            print(f"Kitap eklendi: {book}")
        except Exception as e:
            print(f"Hata: {e}")

    elif cmd == "remove":
        if len(args) != 2:
            print("Kullanım: python main.py remove <ISBN>")
            return
        isbn = args[1]
        if lib.remove_book(isbn):
            print("Kitap silindi.")
        else:
            print("Kitap bulunamadı.")

    elif cmd == "find":
        if len(args) != 2:
            print("Kullanım: python main.py find <ISBN>")
            return
        isbn = args[1]
        book = lib.find_book(isbn)
        if book:
            print(book)
        else:
            print("Kitap bulunamadı.")

    elif cmd == "list":
        kitaplar = lib.list_books()
        if kitaplar:
            for b in kitaplar:
                print("-", b)
        else:
            print("Kütüphane boş.")

    else:
        print("Bilinmeyen komut.")
        print_usage()

if __name__ == "__main__":
    main()
