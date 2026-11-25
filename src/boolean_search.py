import json
from pathlib import Path
from inverted_index import build_inverted_index, show_inverted_index
from query_parser import parse_to_postfix
from textprocessing import lowercased_data


def intersect_postings(postings1, postings2):
    result = []
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
    return result

def union_postings(postings1, postings2):
    result = []
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
    result.extend(postings1[i:])
    result.extend(postings2[j:])
    return result

def not_postings(postings, all_doc_ids):
    result = []
    i,j = 0,0
    while i < len(all_doc_ids) and j < len(postings):
        if all_doc_ids[i] == postings[j]:
            i += 1
            j += 1
        elif all_doc_ids[i] < postings[j]:
            result.append(all_doc_ids[i])
            i += 1
        else:
            j += 1
    result.extend(all_doc_ids[i:])
    return result

def boolean_search(query, inverted_index, all_doc_ids):
    postfix_expression = parse_to_postfix(query)
    stack = []

    for token in postfix_expression:
        match token:
            case "AND":
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: 'AND' requires two operands.")
                right = stack.pop()
                left = stack.pop()
                result = intersect_postings(left, right)
                stack.append(result)
            case "OR":
                if len(stack) < 2:
                    raise ValueError("Invalid syntax: 'OR' requires two operands.")
                right = stack.pop()
                left = stack.pop()
                result = union_postings(left, right)  
                stack.append(result)
            case "NOT":
                if len(stack) < 1:
                    raise ValueError("Invalid syntax: 'NOT' requires one operand.")
                operand = stack.pop()
                result = not_postings(operand, all_doc_ids)
                stack.append(result)
            case _:
                if token in inverted_index:
                    postings = inverted_index[token]["doc_ids"]
                    stack.append(postings)
                else:
                    stack.append([])

    if len(stack) != 1:
        raise ValueError("Invalid syntax, it's missing an operator between terms.")
    return stack[0]

def show_search_results(query, matching_doc_ids, video_lookup):
    print(f"Query: {query}")
    print(f"Number of matching documents: {len(matching_doc_ids)}")

    for rank, vid_id in enumerate(matching_doc_ids, start=1):
        meta= video_lookup.get(vid_id, {})
        title = meta.get("title", "Unknown Title")
        url = meta.get("url", f"https://www.youtube.com/watch?v={vid_id}")
        print(f"{rank}. [{vid_id}] {title}")
        print(f"   URL: {url}")
    print("-" * 40)

if __name__ == "__main__":
    dataset_path = Path(__file__).resolve().parent.parent / "data" / "Dataset.json"
    with open(dataset_path, "r", encoding="utf-8") as file:
        raw_videos = json.load(file)

    video_lookup = {video["video_id"]: video for video in raw_videos}
    all_doc_ids = sorted(video_lookup.keys())
    index = build_inverted_index(lowercased_data)

    test_queries = [
        "artificial AND intelligence",
        "machine OR learning",
        "data AND NOT science",
        "(artificial AND intelligence) OR (machine AND learning)",
        "NOT data",
        "artificial AND (intelligence OR machine) AND NOT data",
        "machine OR robotics",
        "artificial AND NOT robotics",
        "(machine OR deep) AND learning"
    ]

    for query in test_queries:
        matches = boolean_search(query, index, all_doc_ids)
        show_search_results(query, matches, video_lookup)
        
