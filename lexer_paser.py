import re

# Token specifications
TOKEN_SPECIFICATION = [
    ('NUMBER', r'\b\d+(\.\d+)?\b'),  # Numbers (integers and decimals)
    ('STRING', r'"[^"]*"|\'[^\']*\''),  # Strings with single or double quotes
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Variable and function names
    ('OPERATOR', r'[\+\-\*/=]'),  # Arithmetic operators
    ('LPAREN', r'\('),  # Left parenthesis `(`
    ('RPAREN', r'\)'),  # Right parenthesis `)`
    ('LBRACKET', r'\['),  # Left bracket `[`
    ('RBRACKET', r'\]'),  # Right bracket `]`
    ('COMMA', r','),  # Comma `,`
    ('COLON', r':'),  # Colon `:`
    ('NEWLINE', r'\n'),  # Line endings
    ('SKIP', r'[ \t]+'),  # Skip spaces and tabs
    ('MISMATCH', r'.'),  # Catch-all for errors
]

# Lexer function
def tokenize(code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
    get_token = re.compile(token_regex).finditer
    tokens = []
    
    for match in get_token(code):
        kind = match.lastgroup
        value = match.group()
        
        if kind == 'SKIP':
            continue  # Ignore spaces and tabs
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character: {value}")  # Error handling
        
        tokens.append((kind, value))  # Append valid tokens
    
    return tokens

# Simple Parser (Syntax Checker)
def parse(tokens):
    if not tokens:
        raise SyntaxError("Empty input")
    
    index = 0
    while index < len(tokens):
        token_type, token_value = tokens[index]

        if token_type == 'IDENTIFIER' and token_value == 'print':
            # Expecting an opening parenthesis
            if index + 1 < len(tokens) and tokens[index + 1][0] == 'LPAREN':
                index += 2  # Move to the next token after '('
            else:
                raise SyntaxError(f"Expected '(' after 'print', got {tokens[index + 1][1]}")
        
        elif token_type == 'RPAREN':
            # Ensure ')' follows a valid argument
            if index > 0 and tokens[index - 1][0] in ('STRING', 'NUMBER', 'IDENTIFIER'):
                pass  # Valid syntax
            else:
                raise SyntaxError(f"Unexpected closing parenthesis at {token_value}")
        
        index += 1

    print("Syntax Analysis Passed ✔")

# Read processed.py file
with open("processed.py", "r") as f:
    source_code = f.read()

# Tokenization
print("Tokenizing...")
tokens = tokenize(source_code)
print("Tokens:", tokens)

# Parsing
print("Parsing...")
parse(tokens)
