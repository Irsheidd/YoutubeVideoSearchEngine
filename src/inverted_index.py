import math 
from textprocessing import lowercased_data

def create_skips(doc_ids, min_length=10):
    skips = {}
    if len(doc_ids) >= min_length:
        step = int(math.sqrt(len(doc_ids)))
        for i in range(0, len(doc_ids) - step, step):
            skips[i] = i + step
    return skips

def build_inverted_index(documents):
    temp_index={}
    for doc in documents:
        doc_id= doc["video_id"]
        for term in doc["unique_words"]:
            if term not in temp_index:
                temp_index[term] = set()
            temp_index[term].add(doc_id)

    inverted_index = {}
    for term in sorted(temp_index.keys()):
        sorted_doc_ids = sorted(temp_index[term])
        inverted_index[term] = {
            "df": len(sorted_doc_ids),
            "doc_ids": sorted_doc_ids,
            "skips": create_skips(sorted_doc_ids)
        }
    return inverted_index

def show_inverted_index(inverted_index, terms=None):
    print(f"Number of unique terms in the inverted index:{len(inverted_index)}")
    if terms:
        terms_to_display = [t.lower() for t in terms if t.lower() in inverted_index]
    else:
        terms_to_display = sorted(
            inverted_index.keys(),
            key=lambda x: inverted_index[x]["df"],
            reverse=True
        ) [:10]
    for term in terms_to_display:
        print(f"Term: {term}")
        print(f"Document Frequency (df): {inverted_index[term]['df']}")
        print(f"Document IDs: {inverted_index[term]['doc_ids']}\n")

if __name__ == "__main__":
    inverted_index = build_inverted_index(lowercased_data)
    show_inverted_index(inverted_index, terms=["artificial", "intelligence", "machine","learning", "data", "science"])