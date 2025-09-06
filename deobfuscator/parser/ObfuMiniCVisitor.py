# Generated from ObfuMiniC.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ObfuMiniCParser import ObfuMiniCParser
else:
    from ObfuMiniCParser import ObfuMiniCParser

# This class defines a complete generic visitor for a parse tree produced by ObfuMiniCParser.

class ObfuMiniCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ObfuMiniCParser#compilationUnit.
    def visitCompilationUnit(self, ctx:ObfuMiniCParser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#funcDef.
    def visitFuncDef(self, ctx:ObfuMiniCParser.FuncDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#paramList.
    def visitParamList(self, ctx:ObfuMiniCParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#param.
    def visitParam(self, ctx:ObfuMiniCParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#varDecl.
    def visitVarDecl(self, ctx:ObfuMiniCParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#initList.
    def visitInitList(self, ctx:ObfuMiniCParser.InitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#init.
    def visitInit(self, ctx:ObfuMiniCParser.InitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#type.
    def visitType(self, ctx:ObfuMiniCParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#blockStmt.
    def visitBlockStmt(self, ctx:ObfuMiniCParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#stmt.
    def visitStmt(self, ctx:ObfuMiniCParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#exprStmt.
    def visitExprStmt(self, ctx:ObfuMiniCParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#ifStmt.
    def visitIfStmt(self, ctx:ObfuMiniCParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#loopStmt.
    def visitLoopStmt(self, ctx:ObfuMiniCParser.LoopStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#returnStmt.
    def visitReturnStmt(self, ctx:ObfuMiniCParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#ioStmt.
    def visitIoStmt(self, ctx:ObfuMiniCParser.IoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#expr.
    def visitExpr(self, ctx:ObfuMiniCParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#assignExpr.
    def visitAssignExpr(self, ctx:ObfuMiniCParser.AssignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#logicOrExpr.
    def visitLogicOrExpr(self, ctx:ObfuMiniCParser.LogicOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#logicAndExpr.
    def visitLogicAndExpr(self, ctx:ObfuMiniCParser.LogicAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#equalityExpr.
    def visitEqualityExpr(self, ctx:ObfuMiniCParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#relationalExpr.
    def visitRelationalExpr(self, ctx:ObfuMiniCParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#addExpr.
    def visitAddExpr(self, ctx:ObfuMiniCParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#mulExpr.
    def visitMulExpr(self, ctx:ObfuMiniCParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#unaryExpr.
    def visitUnaryExpr(self, ctx:ObfuMiniCParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:ObfuMiniCParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ObfuMiniCParser#argList.
    def visitArgList(self, ctx:ObfuMiniCParser.ArgListContext):
        return self.visitChildren(ctx)



del ObfuMiniCParser