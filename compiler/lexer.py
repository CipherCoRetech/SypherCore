# lexer.py - Lexical Analyzer for SypherLang

import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        # Define patterns for different token types
        patterns = {
            'KEYWORD': r'\b(contract|function|let|public|private|int|string|bool|modifier|throw|emit|event|return|if|else|map|address)\b',
            'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
            'NUMBER': r'\b\d+\b',
            'OPERATOR': r'[+\-*/=<>!&|]+',
            'SYMBOL': r'[{}();,]',
            'STRING_LITERAL': r'\".*?\"'
        }

        # Compile the regex patterns into one
        combined_pattern = '|'.join(f'(?P<{key}>{pattern})' for key, pattern in patterns.items())
        compiled_regex = re.compile(combined_pattern)

        # Find matches in the code
        for match in compiled_regex.finditer(self.code):
            kind = match.lastgroup
            value = match.group()
            self.tokens.append((kind, value))

        return self.tokens

    def __repr__(self):
        return f"Lexer(tokens={self.tokens})"
