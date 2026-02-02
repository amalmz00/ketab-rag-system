import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import subprocess
from tabulate import tabulate

# ===============================
# Load Knowledge Base
# ===============================
df = pd.read_csv("books_all.csv")

# --- فیلتر آیتم‌های غیرکتابی ---
df = df[
    ~df["title"].str.contains("request|browse|form", case=False, na=False)
]

documents = (df["title"] + " " + df["description"]).tolist()

# ===============================
# Retrieval (Semantic Search)
# ===============================
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(documents)

query = input("عبارت جستجو را وارد کنید: ")

query_vec = vectorizer.transform([query])
similarities = cosine_similarity(query_vec, doc_vectors).flatten()

top_indices = similarities.argsort()[-5:][::-1]

# ===============================
# Build Clean Result Table
# ===============================
results = []

for rank, idx in enumerate(top_indices, start=1):
    results.append([
        rank,
        df.iloc[idx]["title"],
        df.iloc[idx]["description"][:150],
        df.iloc[idx]["source"],
        df.iloc[idx]["url"]
    ])

headers = ["رتبه", "عنوان کتاب", "بخشی از متن منبع", "منبع", "لینک"]

# ===============================
# Show Table (Perfect Format)
# ===============================
print("\n📊 نتایج جستجوی معنایی (رتبه‌بندی‌شده):\n")
print(tabulate(results, headers=headers, tablefmt="grid", showindex=False))

# ===============================
# Save Table for Submission
# ===============================
results_df = pd.DataFrame(results, columns=headers)
results_df.to_csv("semantic_search_results.csv", index=False, encoding="utf-8-sig")


# ===============================
# RAG Generation
# ===============================
context = ""
for r in results:
    context += f"- {r[1]}: {r[2]}\n"

prompt = f"""
بر اساس اطلاعات زیر به سوال پاسخ بده:

{context}

سوال:
{query}

پاسخ:
"""

process = subprocess.Popen(
    ["ollama", "run", "qwen2.5:7b"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

stdout, _ = process.communicate(prompt.encode("utf-8"))
answer = stdout.decode("utf-8", errors="ignore")

print("\n🧠 پاسخ نهایی سیستم (RAG):\n")
print(answer)
