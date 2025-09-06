from typing import List, Optional

""" Base AST Node """


class Node:
    pass


class ASTNode:
    def __repr__(self):
        return self._repr()

    def _repr(self, indent=0):
        pad = "  " * indent
        fields = vars(self)
        result = f"{pad}{self.__class__.__name__}:\n"
        for k, v in fields.items():
            result += f"{pad}  {k}: "
            if isinstance(v, ASTNode):
                result += "\n" + v._repr(indent + 2)
            elif isinstance(v, list):
                result += "[\n"
                for item in v:
                    if isinstance(item, ASTNode):
                        result += item._repr(indent + 3) + "\n"
                    else:
                        result += "  " * (indent + 3) + repr(item) + "\n"
                result += pad + "  ]\n"
            else:
                result += repr(v) + "\n"
        return result


""" Program Structure """


class Program(ASTNode):
    def __init__(self, functions: List["Function"]):
        self.functions = functions


class Function(ASTNode):
    def __init__(
        self,
        return_type: str,
        name: str,
        params: List["Parameter"],
        body: List["Statement"],
    ):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body


class Parameter(ASTNode):
    def __init__(self, param_type: str, name: str):
        self.param_type = param_type
        self.name = name


""" Abstract Bases """


class Statement(ASTNode):
    pass


class Expression(ASTNode):
    pass


""" Statements """


class VariableDecl(Statement):
    def __init__(self, var_type: str, name: str, init_expr: Optional[Expression]):
        self.var_type = var_type
        self.name = name
        self.init_expr = init_expr


class ExpressionStmt(Statement):
    def __init__(self, expr: Optional[Expression]):
        self.expr = expr


class Return(Statement):
    def __init__(self, value: Optional[Expression]):
        self.value = value


class IfStmt(Statement):
    def __init__(
        self,
        condition: Expression,
        then_branch: Statement,
        else_branch: Optional[Statement],
    ):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStmt(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body


class ForStmt(Statement):
    def __init__(
        self,
        init: Optional[Expression],
        cond: Optional[Expression],
        update: Optional[Expression],
        body: Statement,
    ):
        self.init = init
        self.cond = cond
        self.update = update
        self.body = body


class Block(Statement):
    def __init__(self, items: List[Statement]):
        self.items = items


class Print(Statement):
    def __init__(self, format_str: str, args: List[Expression]):
        self.format_str = format_str
        self.args = args


class Scan(Statement):
    def __init__(self, format_str: str, args: List[str]):
        self.format_str = format_str
        self.args = args


class Assignment(Statement):
    def __init__(self, target: str, value: Expression):
        self.target = target
        self.value = value


""" Expressions """


class BinaryOp(Expression):
    def __init__(self, op: str, left: Expression, right: Expression):
        self.op = op
        self.left = left
        self.right = right


class UnaryOp(Expression):
    def __init__(self, op: str, operand: Expression):
        self.op = op
        self.operand = operand


class Literal(Expression):
    def __init__(self, value):
        self.value = value


class Variable(Expression):
    def __init__(self, name: str):
        self.name = name


class FuncCall(Expression):
    def __init__(self, name: str, args: List[Expression]):
        self.name = name
        self.args = args


class Label:
    def __init__(self, name):
        self.name = name


class Goto(Node):
    def __init__(self, label):
        self.label = label


class SwitchCase:
    def __init__(self, value, label, body):
        self.value = value
        self.label = label
        self.body = body


class Switch:
    def __init__(self, expr, cases, default=None):
        self.expr = expr
        self.cases = cases
        self.default = default
