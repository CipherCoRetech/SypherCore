# parser.py - Parser for SypherLang

from ast import ContractNode, FunctionNode, LetNode, ParameterNode

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
        return ContractNode(contract_name, contract_body)

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
        return FunctionNode(func_name, parameters, func_body)

    def parse_parameters(self):
        params = []
        while self.tokens[self.current_token][1] != ')':
            param_type = self.consume('KEYWORD')[1]
            param_name = self.consume('IDENTIFIER')[1]
            params.append(ParameterNode(param_type, param_name))
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
        value = self.consume('NUMBER')[1]
        return LetNode(var_name, value)

    def consume(self, token_type, value=None):
        token = self.tokens[self.current_token]
        if token[0] == token_type and (value is None or token[1] == value):
            self.current_token += 1
            return token
        else:
            raise SyntaxError(f"Expected token {token_type} {value}, but got {token}")

    def __repr__(self):
        return f"Parser(ast={self.ast})"
