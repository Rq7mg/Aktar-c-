import os
import json
from pymongo import MongoClient

# Heroku’da Config Vars → MONGO_URI eklenmiş olmalı
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    print("❌ Hata: MONGO_URI environment variable yok!")
    exit()

# MongoDB bağlantısı
client = MongoClient(MONGO_URI)
db = client["tabu_bot"]
words_col = db["words"]

# words.json dosyasını oku
WORDS_FILE = "words.json"
if not os.path.exists(WORDS_FILE):
    print(f"❌ Hata: {WORDS_FILE} bulunamadı!")
    exit()

with open(WORDS_FILE, encoding="utf-8") as f:
    words = json.load(f)

added = 0
for w in words:
    word_lower = w["word"].strip().lower()
    hint = w.get("hint", "").strip()

    # Aynı kelimeyi tekrar ekleme
    if not words_col.find_one({"word": word_lower}):
        words_col.insert_one({"word": word_lower, "hint": hint})
        added += 1

print(f"✅ Toplam {added} kelime MongoDB’ye aktarıldı")
