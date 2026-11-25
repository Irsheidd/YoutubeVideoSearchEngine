import time
from biword_index import build_biword_index, phrase_search
from boolean_search import boolean_search
from inverted_index import build_inverted_index
from query_parser import parse_to_postfix
from skip_pointers import and_search, intersect_count, intersect_with_skips
from textprocessing import lowercased_data

def union_count(postings1, postings2):
    result = []
    comparisons = 0
    i, j = 0, 0
    while i < len(postings1) and j < len(postings2):
        if postings1[i] == postings2[j]:
            result.append(postings1[i])
            i += 1
            j += 1
        elif postings1[i] < postings2[j]:
            result.append(postings1[i])
            i += 1
        else:
            result.append(postings2[j])
            j += 1
        comparisons += 1
    result.extend(postings1[i:])
    result.extend(postings2[j:])
    return result, comparisons

def not_count(postings, all_doc_ids):
    result = []
    comparisons = 0
    i, j = 0, 0
    while i < len(all_doc_ids) and j < len(postings):
        if all_doc_ids[i] == postings[j]:
            i += 1
            j += 1
        elif all_doc_ids[i] < postings[j]:
            result.append(all_doc_ids[i])
            i += 1
        else:
            j += 1
        comparisons += 1
    result.extend(all_doc_ids[i:])
    return result, comparisons

def mixed_search(query, index, all_doc_ids, use_skips):
    empty = {"df": 0, "doc_ids": [], "skips": {}}
    stack = []
    total = 0
    for token in parse_to_postfix(query):
        if token == "NOT":
            postings, skips = stack.pop()
            result, comparisons = not_count(postings, all_doc_ids)
            stack.append((result, {}))
            total += comparisons
        elif token == "OR":
            right, right_skips = stack.pop()
            left, left_skips = stack.pop()
            result, comparisons = union_count(left, right)
            stack.append((result, {}))
            total += comparisons
        elif token == "AND":
            right, right_skips = stack.pop()
            left, left_skips = stack.pop()
            if use_skips:
                result, comparisons = intersect_with_skips(left, left_skips, right, right_skips)
            else:
                result, comparisons = intersect_count(left, right)
            stack.append((result, {}))
            total += comparisons
        else:
            entry = index.get(token, empty)
            stack.append((entry["doc_ids"], entry["skips"]))
    return stack[0][0], total

def measure_time(function, *inputs):
    runs = 1000
    start = time.perf_counter()
    for _ in range(runs):
        function(*inputs)
    end = time.perf_counter()
    return (end - start) / runs * 1_000_000

if __name__ == "__main__":
    index = build_inverted_index(lowercased_data)
    biword_index = build_biword_index(lowercased_data)
    all_doc_ids = sorted(doc["video_id"] for doc in lowercased_data)

    and_queries = [
        "artificial AND intelligence",
        "machine AND learning",
        "ai AND robotics",
        "artificial AND intelligence AND robotics",
        "ai AND learning AND neural",
        "the AND to AND networks"
    ]

    mixed_queries = [
        "machine OR robotics",
        "NOT data",
        "artificial AND NOT robotics",
        "(machine OR deep) AND learning",
        "(neural OR robotics) AND ai",
        "ai AND robotics OR machine AND neural"
    ]

    phrases = [
        ("machine", "learning"),
        ("data", "science"),
        ("computer", "science"),
        ("ai", "tutorial"),
        ("ai", "course")
    ]

    print("PART 1: standard and optimized search")
    print(f"{'Query':<42}{'Matches':>8}{'Std cmp':>9}{'Opt cmp':>9}{'Std us':>9}{'Opt us':>9}  Same")
    for query in and_queries + mixed_queries:
        if query in and_queries:
            _, standard_result, standard = and_search(query, index, False, False)
            _, optimized_result, optimized = and_search(query, index, True, True)
            standard_time = measure_time(and_search, query, index, False, False)
            optimized_time = measure_time(and_search, query, index, True, True)
        else:
            standard_result, standard = mixed_search(query, index, all_doc_ids, False)
            optimized_result, optimized = mixed_search(query, index, all_doc_ids, True)
            standard_time = measure_time(mixed_search, query, index, all_doc_ids, False)
            optimized_time = measure_time(mixed_search, query, index, all_doc_ids, True)

        expected = boolean_search(query, index, all_doc_ids)
        same = standard_result == optimized_result == expected
        print(f"{query:<42}{len(expected):>8}{standard:>9}{optimized:>9}{standard_time:>9.1f}{optimized_time:>9.1f}  {same}")

    print()
    print("PART 2: AND search and biword phrase search")
    print(f"{'Words':<26}{'AND':>6}{'Phrase':>8}{'Only AND':>10}{'AND cmp':>9}{'AND us':>9}{'Phrase us':>11}")
    for word1, word2 in phrases:
        and_query = f"{word1} AND {word2}"
        phrase = f'"{word1} {word2}"'
        _, and_result, comparisons = and_search(and_query, index, False, False)
        phrase_result = phrase_search(phrase, biword_index)
        and_time = measure_time(and_search, and_query, index, False, False)
        phrase_time = measure_time(phrase_search, phrase, biword_index)
        only_and = len(and_result) - len(phrase_result)
        print(f"{word1 + ' ' + word2:<26}{len(and_result):>6}{len(phrase_result):>8}{only_and:>10}{comparisons:>9}{and_time:>9.1f}{phrase_time:>11.1f}")
        