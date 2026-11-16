import json, re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from pathlib import Path


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "Dataset.json"

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

TEXT_FIELDS = ["title", "description", "channel"]

lowercased_data = []
for item in data:
    new_item = item.copy()
    for field in TEXT_FIELDS:
        new_item[field] = re.sub(r"[^\w\s]", " ", new_item[field].lower())
        new_item[field] = new_item[field].split()
    lowercased_data.append(new_item)

first = lowercased_data[:5]
for item in first:
    print(item["title"], "||")


