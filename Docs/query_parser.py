import re
OPERATORS = ["AND", "OR", "NOT"]
PRECEDENCE = {"NOT": 3, "AND": 2, "OR": 1}
def tokenize_query(query):
    raw_tokens= re.findall(r'\w+|AND|OR|NOT|\(|\)', query)
    tokens = []
    for token in raw_tokens:
        upper_token= token.upper()
        if upper_token in OPERATORS or token in ("(", ")"):
            tokens.append(upper_token)
        else:
            cleaned_token= re.sub(r"[^\w\s]", "", token.lower())
            if cleaned_token:
                tokens.append(cleaned_token)
    return tokens

def parse_to_postfix(query):

    tokens =  tokenize_query(query)
    output_queue = []
    operator_stack = []

    for token in tokens:
        if token=="(":
            operator_stack.append(token)
        elif token==")":
            while operator_stack and operator_stack[-1]!="(":
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Mismatched parentheses in the query.")
            operator_stack.pop()  
        elif token in OPERATORS:
            while( operator_stack and operator_stack[-1]!="(" and PRECEDENCE[operator_stack[-1]] >= PRECEDENCE[token]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            output_queue.append(token)

    while operator_stack:
        top = operator_stack.pop()
        if top in ("(", ")"):
            raise ValueError("Mismatched parentheses in the query.")
        output_queue.append(top)
    return output_queue

if __name__ == "__main__":
    query = "artificial AND intelligence OR (machine AND learning) AND NOT data"
    postfix_expression = parse_to_postfix(query)
    print("Postfix Expression:", postfix_expression)