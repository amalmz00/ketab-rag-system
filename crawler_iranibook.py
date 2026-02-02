import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

# صفحه مرور کتاب‌ها (قدیمی و ساده)
url = "https://iranibook.com/book_browse.htm"

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

books = []

# لینک کتاب‌ها معمولاً a ساده هستند
for a in soup.find_all("a", href=True):
    href = a["href"]

    if "book" in href.lower() and href.endswith(".htm"):
        book_url = "https://iranibook.com/" + href

        br = requests.get(book_url, headers=headers)
        bs = BeautifulSoup(br.text, "html.parser")

        title = bs.find("title")
        desc = bs.find("meta", {"name": "description"})

        books.append({
            "title": title.text.strip() if title else "نامشخص",
            "description": desc["content"] if desc else "بدون توضیح",
            "source": "iranibook",
            "url": book_url
        })

        time.sleep(1)

        if len(books) == 5:  # ۵ کتاب کافی است
            break

df = pd.DataFrame(books)
df.to_csv("books_iranibook.csv", index=False, encoding="utf-8-sig")

print("✅ خزش Iranibook انجام شد")
print("تعداد کتاب‌ها:", len(books))
