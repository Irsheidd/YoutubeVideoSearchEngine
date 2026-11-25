import re
OPERATORS = ["AND", "OR", "NOT"]
PRECEDENCE = {"NOT": 3, "AND": 2, "OR": 1}
def tokenize_query(query):
    raw_tokens= re.findall(r'\w+|AND|OR|NOT|\(|\)|\S', query)
    tokens = []
    for token in raw_tokens:
        upper_token= token.upper()
        if upper_token in OPERATORS or token in ("(", ")"):
            tokens.append(upper_token)
        else:
            cleaned_token= re.sub(r"[^\w\s]", "", token.lower())
            if cleaned_token:
                tokens.append(cleaned_token)
            else:
                raise ValueError(f"Invalid token: '{token}'.")
    return tokens

def validate_tokens(tokens):
    expect_operand = True
    for token in tokens:
        if token=="(" or token == "NOT":
            if not expect_operand:
                raise ValueError(f"Expected AND or OR before {token}.")
        elif token==")":
            if expect_operand:
                raise ValueError(f"Expected a word before ')'.")
        elif token in OPERATORS:
            if expect_operand:
                raise ValueError(f"Expected a word before '{token}'.")
            expect_operand = True
        else:
            if not expect_operand:
                raise ValueError(f"Expected AND or OR before '{token}'.")
            expect_operand = False
    if expect_operand:
        raise ValueError("The query is empty or incomplete.")

def parse_to_postfix(query):

    tokens =  tokenize_query(query)
    validate_tokens(tokens)
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
            while( token!= "NOT" and operator_stack and operator_stack[-1]!="(" and PRECEDENCE[operator_stack[-1]] >= PRECEDENCE[token]):
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
    query = ["artificial AND intelligence",
             "machine OR deep",
             "artificial AND NOT robotics",
             "(machine OR deep) AND learning",
             "NOT NOT data", 
             "artificial AND",
             "AND artificial",
             "artificial NOT",
             "artificial machine AND",
             "artificial intelligence",
             "()",
             "",
             "(artificial AND machine",
             "artificial AND & machine"]
    for q in query:
        print(f"Query: {q}")
        try:
            postfix_expression = parse_to_postfix(q)
            print("Valid query. Postfix:", postfix_expression)
        except ValueError as e:
            print(f"Invalid query: {e}")