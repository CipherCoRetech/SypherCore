# ast.py - Abstract Syntax Tree representation for SypherLang

class ASTNode:
    """Base class for AST nodes."""
    def __init__(self, node_type):
        self.node_type = node_type

    def __repr__(self):
        return f"{self.__class__.__name__}({self.node_type})"


class ContractNode(ASTNode):
    """AST node representing a contract."""
    def __init__(self, name, body):
        super().__init__("contract")
        self.name = name
        self.body = body

    def __repr__(self):
        return f"ContractNode(name={self.name}, body={self.body})"


class FunctionNode(ASTNode):
    """AST node representing a function."""
    def __init__(self, name, parameters, body):
        super().__init__("function")
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionNode(name={self.name}, parameters={self.parameters}, body={self.body})"


class LetNode(ASTNode):
    """AST node representing a let statement."""
    def __init__(self, name, value):
        super().__init__("let")
        self.name = name
        self.value = value

    def __repr__(self):
        return f"LetNode(name={self.name}, value={self.value})"


class ParameterNode(ASTNode):
    """AST node representing a parameter in a function."""
    def __init__(self, param_type, param_name):
        super().__init__("parameter")
        self.param_type = param_type
        self.param_name = param_name

    def __repr__(self):
        return f"ParameterNode(type={self.param_type}, name={self.param_name})"
