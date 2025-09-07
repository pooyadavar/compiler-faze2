from deobfuscator.ast import *

class DeadCodeRemover:
    def remove(self, prog: Program):
        for func in prog.functions:
            func.body = self._remove_block(func.body)

    def _remove_block(self, stmts):
        new = []
        for s in stmts:
            # If (0) → dead
            if isinstance(s, IfStmt):
                if isinstance(s.condition, Literal) and s.condition.value == 0:
                    continue
                s.then_branch = self._wrap(s.then_branch)
                if s.else_branch:
                    s.else_branch = self._wrap(s.else_branch)
                new.append(s)

            # Drop unused_* vars entirely
            elif isinstance(s, VariableDecl):
                if s.name.startswith("unused_"):
                    continue
                if s.init_expr:
                    s.init_expr = self._simplify_expr(s.init_expr)
                new.append(s)

            # Drop assignments to unused_*
            elif isinstance(s, Assignment):
                target_name = s.target if isinstance(s.target, str) else getattr(s.target, "name", "")
                if target_name.startswith("unused_"):
                    continue
                s.value = self._simplify_expr(s.value)
                new.append(s)

            # ExpressionStmt cleanup
            elif isinstance(s, ExpressionStmt):
                if s.expr is None: 
                    continue
                if isinstance(s.expr, Literal): 
                    continue
                if isinstance(s.expr, Variable) and s.expr.name.startswith("unused_"):
                    continue
                if isinstance(s.expr, Assignment):
                    target_name = s.expr.target if isinstance(s.expr.target, str) else getattr(s.expr.target, "name", "")
                    if target_name.startswith("unused_"):
                        continue
                s.expr = self._simplify_expr(s.expr)
                new.append(s)

            elif isinstance(s, Block):
                s.items = self._remove_block(s.items)
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

            else:
                new.append(s)
        return new

    def _wrap(self, s):
        if isinstance(s, Block):
            s.items = self._remove_block(s.items)
            return s
        return Block(self._remove_block([s]))

    def _simplify_expr(self, expr):
        if expr is None: return None
        if isinstance(expr, Variable) and expr.name.startswith("unused_"):
            return None
        if isinstance(expr, BinaryOp):
            return BinaryOp(expr.op, self._simplify_expr(expr.left), self._simplify_expr(expr.right))
        if isinstance(expr, UnaryOp):
            return UnaryOp(expr.op, self._simplify_expr(expr.operand))
        if isinstance(expr, FuncCall):
            return FuncCall(expr.name, [self._simplify_expr(a) for a in expr.args if a])
        if isinstance(expr, Assignment):
            target_name = expr.target if isinstance(expr.target, str) else getattr(expr.target, "name", "")
            if target_name.startswith("unused_"):
                return None
            return Assignment(expr.target, self._simplify_expr(expr.value))
        return expr
