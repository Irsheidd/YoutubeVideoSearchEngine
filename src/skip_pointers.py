from query_parser import tokenize_query, validate_tokens
from boolean_search import boolean_search
from inverted_index import build_inverted_index
from textprocessing import lowercased_data

def intersect_count(postings1, postings2):
    result = []
    comparisons = 0
    i, j = 0, 0
    while i < len(postings1) and j < len(postings2):
        if postings1[i] == postings2[j]:
            result.append(postings1[i])
            i += 1
            j += 1
        elif postings1[i] < postings2[j]:
            i += 1
        else:
            j += 1
        comparisons += 1
    return result, comparisons

def intersect_with_skips(postings1, skips1, postings2, skips2):
    result = []
    comparisons = 0
    i, j = 0, 0
    while i < len(postings1) and j < len(postings2):
        if postings1[i] == postings2[j]:
            result.append(postings1[i])
            i += 1
            j += 1
        elif postings1[i] < postings2[j]:
            if i in skips1:
                comparisons += 1
                if postings1[skips1[i]] <= postings2[j]:
                    i = skips1[i]
                else:
                    i += 1
            else:
                i += 1
        else:
            if j in skips2:
                comparisons += 1
                if postings2[skips2[j]] <= postings1[i]:
                    j = skips2[j]
                else:
                    j += 1
            else:
                j += 1
        comparisons += 1
    return result, comparisons

def and_search(query, index, optimize, use_skips):
    tokens = tokenize_query(query)
    validate_tokens(tokens)

    for token in tokens:
        if token in ("OR", "NOT", "(", ")"):
            raise ValueError("and_search only supports AND.")

    words = []
    for token in tokens:
        if token != "AND":
            words.append(token)

    # Piece 4: shortest list first
    empty = {"df": 0, "doc_ids": [], "skips": {}}
    if optimize:
        words.sort(key=lambda word: index.get(word, empty)["df"])

    # Piece 5: start with the first word
    first = index.get(words[0], empty)
    result = first["doc_ids"]
    result_skips = first["skips"]
    total = 0

    # Piece 6: intersect with each remaining word
    for word in words[1:]:
        if not result:
            break
        entry = index.get(word, empty)
        if use_skips:
            result, comparisons = intersect_with_skips(result, result_skips, entry["doc_ids"], entry["skips"])
        else:
            result, comparisons = intersect_count(result, entry["doc_ids"])
        result_skips = {}
        total += comparisons

    return words, result, total


if __name__ == "__main__":
    
    index = build_inverted_index(lowercased_data)
    all_doc_ids = sorted(doc["video_id"] for doc in lowercased_data)

    test_queries = [
        "artificial AND intelligence",
        "artificial AND intelligence AND robotics",
        "machine AND learning",
        "ai AND robotics",
        "ai AND learning AND neural"
    ]

    for query in test_queries:
        _, result1, normal = and_search(query, index, False, False)
        _, result2, skips = and_search(query, index, False, True)
        order, result3, optimized = and_search(query, index, True, False)
        _, result4, both = and_search(query, index, True, True)
        expected = boolean_search(query, index, all_doc_ids)
        same = result1 == result2 == result3 == result4 == expected
        print(f"Query: {query}")
        print(f"Optimized order: {order}")
        print(f"Matching documents: {len(expected)}")
        print(f"Comparisons: normal={normal}, skips={skips}, optimized={optimized}, both={both}")
        print(f"Same results as Boolean search: {same}")
        print("-" * 40)