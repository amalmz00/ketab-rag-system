import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# خواندن داده‌ها
df = pd.read_csv("books_all.csv")

texts = (df["title"] + " " + df["description"]).tolist()

# ساخت مدل TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# گرفتن ورودی از کاربر
query = input("چی کتابی میخوای؟: ")

query_vec = vectorizer.transform([query])

# محاسبه شباهت
similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

# گرفتن 5 نتیجه برتر
top_indices = similarities.argsort()[-5:][::-1]

print("\n🔍 نتایج جستجو:\n")

for rank, idx in enumerate(top_indices):
    print(f"رتبه {rank + 1}")
    print("عنوان:", df.iloc[idx]["title"])
    print("منبع:", df.iloc[idx]["source"])
    print("بخشی از توضیح:", df.iloc[idx]["description"])
    print("لینک:", df.iloc[idx]["url"])
    print("-" * 40)
