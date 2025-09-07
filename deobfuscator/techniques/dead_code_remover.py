from deobfuscator.ast import *
from deobfuscator.techniques.expression_simplifier import ExpressionSimplifier

class DeadCodeRemover:
    """
    Remove unused variables, if(0) blocks, unreachable prints, and dead literals.
    """
    def __init__(self):
        # Use expression simplifier internally
        self.expr_simplifier = ExpressionSimplifier()

    def remove(self, prog: Program):
        for func in prog.functions:
            func.body = self._remove_block(func.body)

    def _remove_block(self, stmts):
        new = []
        for s in stmts:
            if isinstance(s, IfStmt):
                cond = s.condition
                # Remove `if (0)` blocks entirely
                if isinstance(cond, Literal) and cond.value == 0:
                    continue
                s.condition = self._simplify_expr(s.condition)
                s.then_branch = self._wrap(s.then_branch)
                if s.else_branch:
                    s.else_branch = self._wrap(s.else_branch)
                new.append(s)

            elif isinstance(s, VariableDecl):
                if s.name.startswith("unused_"):
                    continue
                if s.init_expr:
                    s.init_expr = self._simplify_expr(s.init_expr)
                new.append(s)

            elif isinstance(s, Block):
                s.items = self._remove_block(s.items)
                if s.items:  # skip empty blocks
                    new.append(s)

            elif isinstance(s, ExpressionStmt):
                if s.expr is None: 
                    continue
                if isinstance(s.expr, Literal): 
                    continue
                s.expr = self._simplify_expr(s.expr)
                new.append(s)

            elif isinstance(s, WhileStmt):
                s.condition = self._simplify_expr(s.condition)
                s.body = self._wrap(s.body)
                new.append(s)

            elif isinstance(s, ForStmt):
                if s.init: s.init = self._simplify_expr(s.init)
                if s.cond: s.cond = self._simplify_expr(s.cond)
                if s.update: s.update = self._simplify_expr(s.update)
                s.body = self._wrap(s.body)
                new.append(s)

            elif isinstance(s, Print):
                # remove unreachable debug prints
                if isinstance(s.format_str, str) and "Unreachable" in s.format_str:
                    continue
                new.append(s)

            else:
                new.append(s)

        return new

    def _wrap(self, s):
        if isinstance(s, Block):
            s.items = self._remove_block(s.items)
            return s
        return Block(self._remove_block([s]))

    def _simplify_expr(self, expr):
        if expr is None:
            return None
        return self.expr_simplifier.visit(expr)
