from deobfuscator.ast import *


class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output = []

    def emit(self, code):
        self.output.append("    " * self.indent_level + code)

    def generate(self, program):
        for func in program.functions:
            self.visit(func)
        return "\n".join(self.output)

    def visit(self, node):
        if isinstance(node, Program):
            for func in node.functions:
                self.visit(func)

        elif isinstance(node, Function):
            params = ", ".join([f"{p.param_type} {p.name}" for p in node.params])
            self.emit(f"{node.return_type} {node.name}({params}) {{")
            self.indent_level += 1
            for stmt in node.body:
                self.visit(stmt)
            self.indent_level -= 1
            self.emit("}")

        elif isinstance(node, VariableDecl):
            if node.init_expr:
                expr = self.visit_expr(node.init_expr)
                self.emit(f"{node.var_type} {node.name} = {expr};")
            else:
                self.emit(f"{node.var_type} {node.name};")

        elif isinstance(node, Assignment):
            expr = self.visit_expr(node.value)
            target = (
                node.target.name
                if isinstance(node.target, Variable)
                else str(node.target)
            )
            self.emit(f"{target} = {expr};")

        elif isinstance(node, Return):
            expr = self.visit_expr(node.value)
            self.emit(f"return {expr};")

        elif isinstance(node, IfStmt):
            cond = self.visit_expr(node.condition)
            self.emit(f"if ({cond})")
            self.visit(node.then_branch)
            if node.else_branch:
                self.emit("else")
                self.visit(node.else_branch)

        elif isinstance(node, WhileStmt):
            cond = self.visit_expr(node.condition)
            self.emit(f"while ({cond})")
            self.visit(node.body)

        elif isinstance(node, ForStmt):
            init = self.visit_expr(node.init) if node.init else ""
            cond = self.visit_expr(node.cond) if node.cond else ""
            update = self.visit_expr(node.update) if node.update else ""
            self.emit(f"for ({init}; {cond}; {update})")
            self.visit(node.body)

        elif isinstance(node, Block):
            self.emit("{")
            self.indent_level += 1
            for stmt in node.items:
                self.visit(stmt)
            self.indent_level -= 1
            self.emit("}")

        elif isinstance(node, ExpressionStmt):
            expr = self.visit_expr(node.expr)
            self.emit(f"{expr};")

        elif isinstance(node, Print):
            if node.args:
                args = ", ".join([self.visit_expr(arg) for arg in node.args])
                self.emit(f'printf("{node.format_str}", {args});')
            else:
                self.emit(f'printf("{node.format_str}");')

        elif isinstance(node, Label):
            self.indent_level = max(0, self.indent_level - 1)
            self.emit(f"{node.name}:")
            self.indent_level += 1

        elif isinstance(node, Goto):
            self.emit(f"goto {node.label};")

        elif isinstance(node, Switch):
            expr = self.visit_expr(node.expr)
            self.emit(f"switch ({expr}) {{")
            self.indent_level += 1
            for case in node.cases:
                case_value = self.visit_expr(case.value)
                self.emit(f"case {case_value}: goto {case.label.name};")
            self.indent_level -= 1
            self.emit("}")

        else:
            self.emit(f"// Unknown node: {type(node).__name__}")

    def visit_expr(self, expr):
        if isinstance(expr, Literal):
            if isinstance(expr.value, str):
                escaped = (
                    expr.value.replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                )
                return f'"{escaped}"'
            else:
                return str(expr.value)

        elif isinstance(expr, Variable):
            return expr.name

        elif isinstance(expr, BinaryOp):
            left = self.visit_expr(expr.left)
            right = self.visit_expr(expr.right)
            return f"({left} {expr.op} {right})"

        elif isinstance(expr, UnaryOp):
            operand = self.visit_expr(expr.operand)
            return f"({expr.op}{operand})"

        elif isinstance(expr, FuncCall):
            args = ", ".join([self.visit_expr(arg) for arg in expr.args])
            return f"{expr.name}({args})"

        elif isinstance(expr, Assignment):
            target = (
                expr.target.name
                if isinstance(expr.target, Variable)
                else str(expr.target)
            )
            value = self.visit_expr(expr.value)
            return f"{target} = {value}"
        else:
            return f"/* Unknown expr: {type(expr).__name__} */"
