import pandas as pd

df1 = pd.read_csv("books_taaghche.csv")
df2 = pd.read_csv("books_iranibook.csv")

df_all = pd.concat([df1, df2], ignore_index=True)
df_all.to_csv("books_all.csv", index=False, encoding="utf-8-sig")

print("✅ پایگاه دانش نهایی ساخته شد")
print("تعداد کل کتاب‌ها:", len(df_all))