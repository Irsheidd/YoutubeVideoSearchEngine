import re
from boolean_search import boolean_search
from inverted_index import build_inverted_index
from textprocessing import lowercased_data

def make_biwords(words):
    biwords = []
    for i in range(len(words) - 1):
        biwords.append(words[i] + " " + words[i + 1])
    return biwords

def build_biword_index(documents):
    temp_index = {}
    for doc in documents:
        doc_id = doc["video_id"]
        for field in ["title", "description"]:
            for biword in make_biwords(doc[field]):
                if biword not in temp_index:
                    temp_index[biword] = set()
                temp_index[biword].add(doc_id)

    biword_index = {}
    for biword in sorted(temp_index.keys()):
        sorted_doc_ids = sorted(temp_index[biword])
        biword_index[biword] = {
            "df": len(sorted_doc_ids),
            "doc_ids": sorted_doc_ids
        }
    return biword_index

def phrase_search(query, biword_index):
    query = query.strip()
    if len(query) < 2 or not (query.startswith('"') and query.endswith('"')):
        raise ValueError("A phrase must be inside double quotes.")

    words = re.findall(r"\w+", query.lower())
    if len(words) != 2:
        raise ValueError("A phrase must have exactly two words.")

    biword = words[0] + " " + words[1]
    if biword in biword_index:
        return biword_index[biword]["doc_ids"]
    return []

if __name__ == "__main__":
    index = build_inverted_index(lowercased_data)
    biword_index = build_biword_index(lowercased_data)
    all_doc_ids = sorted(doc["video_id"] for doc in lowercased_data)
    titles = {doc["video_id"]: " ".join(doc["title"]) for doc in lowercased_data}

    print(make_biwords(["introduction", "to", "machine", "learning"]))
    print(f"Number of unique biwords: {len(biword_index)}")
    print("-" * 40)

    test_phrases = [
        ("machine", "learning"),
        ("artificial", "intelligence"),
        ("data", "science"),
        ("computer", "science"),
        ("ai", "tutorial"),
        ("ai", "course")
    ]

    for word1, word2 in test_phrases:
        and_result = boolean_search(f"{word1} AND {word2}", index, all_doc_ids)
        phrase_result = phrase_search(f'"{word1} {word2}"', biword_index)
        only_and = [doc_id for doc_id in and_result if doc_id not in phrase_result]

        print(f"{word1} AND {word2}: {len(and_result)} videos")
        print(f'"{word1} {word2}": {len(phrase_result)} videos')
        print(f"Found only by AND: {len(only_and)}")
        for doc_id in only_and[:3]:
            print(f"  [{doc_id}] {titles[doc_id]}")
        print("-" * 40)