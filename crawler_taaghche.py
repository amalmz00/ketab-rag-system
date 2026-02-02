import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://taaghche.com/category/fiction"

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

books = []

links = soup.find_all("a", href=True)

for a in links:
    href = a["href"]
    if href.startswith("/book/"):
        book_url = "https://taaghche.com" + href

        br = requests.get(book_url, headers=headers)
        bs = BeautifulSoup(br.text, "html.parser")

        title = bs.find("h1")
        desc = bs.find("meta", {"name": "description"})

        books.append({
            "title": title.text.strip() if title else "نامشخص",
            "description": desc["content"] if desc else "بدون توضیح",
            "source": "taaghche",
            "url": book_url
        })

        time.sleep(1)

        if len(books) == 10:
            break

df = pd.DataFrame(books)
df.to_csv("books_taaghche.csv", index=False, encoding="utf-8-sig")

print("✅ خزش طاقچه انجام شد")
print("تعداد کتاب‌ها:", len(books))
