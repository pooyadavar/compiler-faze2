
from deobfuscator.ast import *

class ExpressionSimplifier:
    def visit(self, node):
        if node is None:
            return None
        
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for field, value in vars(node).items():
            if isinstance(value, list):
                new_list = []
                for item in value:
                    new_item = self.visit(item)
                    if new_item:
                        new_list.append(new_item)
                setattr(node, field, new_list)
            elif isinstance(value, (Program, Function, VariableDecl, BinaryOp, UnaryOp, Literal, IfStmt, WhileStmt, ForStmt, Block, Return, ExpressionStmt, Print, Assignment)):
                setattr(node, field, self.visit(value))
        return node

    def visit_BinaryOp(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        
        if (node.op == '-' and 
            isinstance(node.right, UnaryOp) and node.right.op == '-'):
            print("INFO: Simplifying pattern a - (-b) to a + b")
            return BinaryOp('+', node.left, node.right.operand)
        
        if (node.op == '+' and 
            isinstance(node.right, Literal) and node.right.value == 0):
            print("INFO: Simplifying pattern a + 0 to a")
            return node.left

        return node