from deobfuscator.parser.ObfuMiniCVisitor import ObfuMiniCVisitor
from deobfuscator.parser.ObfuMiniCParser import *
from deobfuscator.ast import (
    Program,
    Function,
    Parameter,
    VariableDecl,
    ExpressionStmt,
    Return,
    IfStmt,
    WhileStmt,
    ForStmt,
    Block,
    Print,
    Scan,
    Assignment,
    BinaryOp,
    UnaryOp,
    FuncCall,
    Variable,
    Literal,
    Goto,
    Label,
    Switch,
    SwitchCase 
)


class ASTBuilder(ObfuMiniCVisitor):
    def visitSwitchStmt(self, ctx):
        expr = self.visit(ctx.expr())
        cases = []
        default = None
        label_counter = 0

        for block in ctx.switchBlock():
            if block.caseBlock():
                case_ctx = block.caseBlock()
                value = self.visit(case_ctx.literal())
                label_name = f"case_{label_counter}"
                label_counter += 1
                label = Label(label_name)
                stmts = []
                for stmt_ctx in case_ctx.stmt():
                    stmts.append(self.visit(stmt_ctx))
                body = Block(stmts)
                cases.append(SwitchCase(value, label, body))
            elif block.defaultBlock():
                default_ctx = block.defaultBlock()
                stmts = []
                for stmt_ctx in default_ctx.stmt():
                    stmts.append(self.visit(stmt_ctx))
                default = Block(stmts)

        return Switch(expr, cases, default)
    
    def visitLiteral(self, ctx: ObfuMiniCParser.LiteralContext):
        if ctx.NUMBER():

            value = int(ctx.NUMBER().getText())
            return Literal(value)
        elif ctx.CHAR():
            value = ctx.CHAR().getText()
            return Literal(value)
        elif ctx.BOOL():
            value = ctx.BOOL().getText() == 'true'
            return Literal(value)
        
        return None

    def visitCaseBlock(self, ctx):
        value = self.visit(ctx.literal())
        label_name = f"case_{value}"
        label = Label(label_name)
        stmt = self.visit(ctx.stmt())
        return SwitchCase(value, label)

    def visitLabelStmt(self, ctx):
        name = ctx.ID().getText()
        return Label(name)

    def visitCompilationUnit(self, ctx):
        functions = []
        for child in ctx.children:
            result = self.visit(child)
            if isinstance(result, Function):
                functions.append(result)
        return Program(functions)

    def visitFuncDef(self, ctx):
        return_type = ctx.type_().getText()
        name = ctx.ID().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        block = self.visit(ctx.blockStmt())
        return Function(
            return_type, name, params, block.items if isinstance(block, Block) else []
        )

    def visitParamList(self, ctx):
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx):
        return Parameter(ctx.type_().getText(), ctx.ID().getText())

    def visitBlockStmt(self, ctx):
        stmts = []
        for child in ctx.children[1:-1]:
            result = self.visit(child)
            if result is None:
                continue
            if isinstance(result, list):
                stmts.extend(result)
            else:
                stmts.append(result)
        return Block(stmts)

    def visitVarDecl(self, ctx):
        var_type = ctx.type_().getText()
        decls = []
        for init in ctx.initList().init():
            name = init.ID().getText()
            expr = self.visit(init.expr()) if init.expr() else None
            decls.append(VariableDecl(var_type, name, expr))
        return decls

    def visitExprStmt(self, ctx):
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ExpressionStmt(expr)

    def visitReturnStmt(self, ctx):
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return Return(expr)

    def visitIfStmt(self, ctx):
        cond = self.visit(ctx.expr())
        then_branch = self.visit(ctx.stmt(0))
        else_branch = self.visit(ctx.stmt(1)) if ctx.ELSE() else None
        return IfStmt(cond, then_branch, else_branch)

    def visitLoopStmt(self, ctx):
        if ctx.WHILE():
            cond = self.visit(ctx.expr(0))
            body = self.visit(ctx.stmt())
            return WhileStmt(cond, body)
        else:
            init = self.visit(ctx.expr(0)) if ctx.expr(0) else None
            cond = self.visit(ctx.expr(1)) if ctx.expr(1) else None
            update = self.visit(ctx.expr(2)) if ctx.expr(2) else None
            body = self.visit(ctx.stmt())
            return ForStmt(init, cond, update, body)

    def visitIoStmt(self, ctx):
        if ctx.PRINTF():
            fmt = ctx.STRING().getText().strip('"')
            args = [self.visit(e) for e in ctx.expr()]
            return Print(fmt, args)
        elif ctx.SCANF():
            fmt = ctx.STRING().getText().strip('"')
            args = [tok.getText().replace("&", "") for tok in ctx.ID()]
            return Scan(fmt, args)

    # === Expressions ===

    def visitAssignExpr(self, ctx):
        if ctx.getChildCount() == 3:
            target_text = ctx.getChild(0).getText()
            target_node = Variable(target_text)   # ALWAYS use Variable
            value_node = self.visit(ctx.assignExpr())
            return Assignment(target_node, value_node)
        return self.visit(ctx.logicOrExpr())

    def visitLogicOrExpr(self, ctx):
        if len(ctx.logicAndExpr()) == 1:
            return self.visit(ctx.logicAndExpr(0))
        left = self.visit(ctx.logicAndExpr(0))
        for i in range(1, len(ctx.logicAndExpr())):
            right = self.visit(ctx.logicAndExpr(i))
            left = BinaryOp("||", left, right)
        return left

    def visitLogicAndExpr(self, ctx):
        if len(ctx.equalityExpr()) == 1:
            return self.visit(ctx.equalityExpr(0))
        left = self.visit(ctx.equalityExpr(0))
        for i in range(1, len(ctx.equalityExpr())):
            right = self.visit(ctx.equalityExpr(i))
            left = BinaryOp("&&", left, right)
        return left

    def visitEqualityExpr(self, ctx):
        left = self.visit(ctx.relationalExpr(0))
        for i in range(1, len(ctx.relationalExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.relationalExpr(i))
            left = BinaryOp(op, left, right)
        return left

    def visitRelationalExpr(self, ctx):
        left = self.visit(ctx.addExpr(0))
        for i in range(1, len(ctx.addExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.addExpr(i))
            left = BinaryOp(op, left, right)
        return left

    def visitAddExpr(self, ctx):
        left = self.visit(ctx.mulExpr(0))
        for i in range(1, len(ctx.mulExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.mulExpr(i))
            left = BinaryOp(op, left, right)
        return left

    def visitMulExpr(self, ctx):
        left = self.visit(ctx.unaryExpr(0))
        for i in range(1, len(ctx.unaryExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.unaryExpr(i))
            left = BinaryOp(op, left, right)
        return left

    def visitUnaryExpr(self, ctx):
        if ctx.getChildCount() == 2:
            op = ctx.getChild(0).getText()
            operand = self.visit(ctx.unaryExpr())
            return UnaryOp(op, operand)
        return self.visit(ctx.primaryExpr())

    def visitPrimaryExpr(self, ctx):
        if ctx.ID() and ctx.LPAREN():
            name = ctx.ID().getText()
            args = self.visit(ctx.argList()) if ctx.argList() else []
            return FuncCall(name, args)

        if ctx.ID() and ctx.expr():
            return FuncCall(
                ctx.ID().getText(), self.visit(ctx.argList()) if ctx.argList() else []
            )
        elif ctx.ID():
            return Variable(ctx.ID().getText())
        elif ctx.NUMBER():
            return Literal(int(ctx.NUMBER().getText()))
        elif ctx.BOOL():
            return Literal(ctx.BOOL().getText() == "true")
        elif ctx.CHAR():
            return Literal(ctx.CHAR().getText().strip("'"))
        elif ctx.STRING():
            return Literal(ctx.STRING().getText().strip('"'))
        elif ctx.expr():
            return self.visit(ctx.expr())
        else:
            return None

    def visitArgList(self, ctx):
        return [self.visit(e) for e in ctx.expr()]
    

    def visitGotoStmt(self, ctx: ObfuMiniCParser.GotoStmtContext):
        label_name = ctx.ID().getText()
        return Goto(label_name)

    def visitLabelStmt(self, ctx: ObfuMiniCParser.LabelStmtContext):
        label_name = ctx.ID().getText()
        return Label(label_name)
