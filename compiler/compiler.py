import re
import sys
import os

# -------------------------
# Lexical Analysis - Tokenizer
# -------------------------
class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
    
    def tokenize(self):
        patterns = {
            'KEYWORD': r'\b(contract|function|let|public|private|if|else|return|modifier|throw|emit|for|while|map|address|int|string|bool|constructor|event)\b',
            'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
            'NUMBER': r'\b\d+\b',
            'OPERATOR': r'[+\-*/=><!]+',
            'SYMBOL': r'[{}();,]',
            'STRING_LITERAL': r'\".*?\"'
        }

        combined_pattern = '|'.join(f'(?P<{key}>{pattern})' for key, pattern in patterns.items())
        compiled_regex = re.compile(combined_pattern)

        for match in compiled_regex.finditer(self.code):
            kind = match.lastgroup
            value = match.group()
            self.tokens.append((kind, value))

        return self.tokens

# -------------------------
# Syntax Analysis - Parser
# -------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        self.ast = []

    def parse(self):
        while self.current_token < len(self.tokens):
            token = self.tokens[self.current_token]
            if token[0] == 'KEYWORD' and token[1] == 'contract':
                self.ast.append(self.parse_contract())
            else:
                raise SyntaxError(f"Unexpected token: {token}")
        return self.ast

    def parse_contract(self):
        self.consume('KEYWORD', 'contract')
        contract_name = self.consume('IDENTIFIER')[1]
        self.consume('SYMBOL', '{')
        contract_body = self.parse_contract_body()
        self.consume('SYMBOL', '}')
        return {
            'type': 'contract',
            'name': contract_name,
            'body': contract_body
        }

    def parse_contract_body(self):
        body = []
        while self.tokens[self.current_token][1] != '}':
            if self.tokens[self.current_token][0] == 'KEYWORD' and self.tokens[self.current_token][1] == 'function':
                body.append(self.parse_function())
            else:
                raise SyntaxError(f"Unexpected token in contract body: {self.tokens[self.current_token]}")
        return body

    def parse_function(self):
        self.consume('KEYWORD', 'function')
        func_name = self.consume('IDENTIFIER')[1]
        self.consume('SYMBOL', '(')
        parameters = self.parse_parameters()
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', '{')
        func_body = self.parse_function_body()
        self.consume('SYMBOL', '}')
        return {
            'type': 'function',
            'name': func_name,
            'parameters': parameters,
            'body': func_body
        }

    def parse_parameters(self):
        params = []
        while self.tokens[self.current_token][1] != ')':
            param_type = self.consume('KEYWORD')[1]
            param_name = self.consume('IDENTIFIER')[1]
            params.append((param_type, param_name))
            if self.tokens[self.current_token][1] == ',':
                self.consume('SYMBOL', ',')
        return params

    def parse_function_body(self):
        body = []
        while self.tokens[self.current_token][1] != '}':
            token = self.tokens[self.current_token]
            if token[0] == 'KEYWORD' and token[1] == 'let':
                body.append(self.parse_let())
            else:
                raise SyntaxError(f"Unexpected token in function body: {token}")
        return body

    def parse_let(self):
        self.consume('KEYWORD', 'let')
        var_name = self.consume('IDENTIFIER')[1]
        self.consume('OPERATOR', '=')
        value = self.consume('NUMBER')[1]  # For simplicity, assuming it's always a number
        return {
            'type': 'let',
            'name': var_name,
            'value': value
        }

    def consume(self, token_type, value=None):
        token = self.tokens[self.current_token]
        if token[0] == token_type and (value is None or token[1] == value):
            self.current_token += 1
            return token
        else:
            raise SyntaxError(f"Expected token {token_type} {value}, but got {token}")

# -------------------------
# Code Generation
# -------------------------
class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.bytecode = []

    def generate(self):
        for node in self.ast:
            if node['type'] == 'contract':
                self.generate_contract(node)
        return self.bytecode

    def generate_contract(self, contract_node):
        self.bytecode.append(f"CONTRACT {contract_node['name']}")
        for function in contract_node['body']:
            self.generate_function(function)
        self.bytecode.append("END CONTRACT")

    def generate_function(self, function_node):
        self.bytecode.append(f"FUNCTION {function_node['name']}")
        for param in function_node['parameters']:
            self.bytecode.append(f"PARAM {param[0]} {param[1]}")
        for statement in function_node['body']:
            self.generate_statement(statement)
        self.bytecode.append("END FUNCTION")

    def generate_statement(self, statement_node):
        if statement_node['type'] == 'let':
            self.bytecode.append(f"LET {statement_node['name']} = {statement_node['value']}")
        else:
            raise ValueError(f"Unsupported statement type: {statement_node['type']}")

# -------------------------
# Compilation Workflow
# -------------------------
def compile_sypher(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    with open(file_path, 'r') as file:
        code = file.read()

    # Lexical Analysis
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)

    # Syntax Analysis
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    # Code Generation
    codegen = CodeGenerator(ast)
    bytecode = codegen.generate()
    print("Bytecode:", bytecode)

    # Save bytecode to file
    bytecode_file = file_path.replace('.sypher', '.bytecode')
    with open(bytecode_file, 'w') as bc_file:
        for line in bytecode:
            bc_file.write(line + '\n')

    print(f"Compilation successful. Bytecode saved to '{bytecode_file}'")

# -------------------------
# Main Entry Point
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <path_to_sypher_contract>")
    else:
        compile_sypher(sys.argv[1])
