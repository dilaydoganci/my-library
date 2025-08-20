# My Library 📚

Bu proje, kullanıcıların terminalden veya FastAPI aracılığıyla kitap ekleyip listeleyebileceği bir Python uygulamasıdır.

---

## 🚀 Kurulum

```bash
git clone https://github.com/dilaydoganci/my-library.git
cd my-library
pip install -r requirements.txt
```

---

## ⚙️ Kullanım

### 🖥 Terminal Uygulaması

```bash
python main.py
```

### 🌐 FastAPI Sunucusu

```bash
uvicorn api:app --reload
```

📄 API dokümantasyonu: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 API Endpointleri

### `GET /books`

Tüm kitapları listeler.

---

### `POST /books`

Yeni bir kitap ekler.

**Örnek Body:**

```json
{
  "title": "Example Book",
  "author": "Jane Doe",
  "isbn": "9781234567890"
}
```

---

### `DELETE /books/{isbn}`

Belirtilen ISBN numarasına sahip kitabı siler.

---

## 🧪 Test

```bash
pytest
```

---

## 📂 Notlar

- `library.json` dosyası, kitaplarınızı yerel olarak saklamak için kullanılır.
- `main.py`, terminal arayüzüdür.
- `api.py`, FastAPI servisidir.
