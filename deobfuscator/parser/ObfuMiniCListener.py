# Generated from ObfuMiniC.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ObfuMiniCParser import ObfuMiniCParser
else:
    from ObfuMiniCParser import ObfuMiniCParser

# This class defines a complete listener for a parse tree produced by ObfuMiniCParser.
class ObfuMiniCListener(ParseTreeListener):

    # Enter a parse tree produced by ObfuMiniCParser#compilationUnit.
    def enterCompilationUnit(self, ctx:ObfuMiniCParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#compilationUnit.
    def exitCompilationUnit(self, ctx:ObfuMiniCParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#funcDef.
    def enterFuncDef(self, ctx:ObfuMiniCParser.FuncDefContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#funcDef.
    def exitFuncDef(self, ctx:ObfuMiniCParser.FuncDefContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#paramList.
    def enterParamList(self, ctx:ObfuMiniCParser.ParamListContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#paramList.
    def exitParamList(self, ctx:ObfuMiniCParser.ParamListContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#param.
    def enterParam(self, ctx:ObfuMiniCParser.ParamContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#param.
    def exitParam(self, ctx:ObfuMiniCParser.ParamContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#varDecl.
    def enterVarDecl(self, ctx:ObfuMiniCParser.VarDeclContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#varDecl.
    def exitVarDecl(self, ctx:ObfuMiniCParser.VarDeclContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#initList.
    def enterInitList(self, ctx:ObfuMiniCParser.InitListContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#initList.
    def exitInitList(self, ctx:ObfuMiniCParser.InitListContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#init.
    def enterInit(self, ctx:ObfuMiniCParser.InitContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#init.
    def exitInit(self, ctx:ObfuMiniCParser.InitContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#type.
    def enterType(self, ctx:ObfuMiniCParser.TypeContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#type.
    def exitType(self, ctx:ObfuMiniCParser.TypeContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#blockStmt.
    def enterBlockStmt(self, ctx:ObfuMiniCParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#blockStmt.
    def exitBlockStmt(self, ctx:ObfuMiniCParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#stmt.
    def enterStmt(self, ctx:ObfuMiniCParser.StmtContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#stmt.
    def exitStmt(self, ctx:ObfuMiniCParser.StmtContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#exprStmt.
    def enterExprStmt(self, ctx:ObfuMiniCParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#exprStmt.
    def exitExprStmt(self, ctx:ObfuMiniCParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#ifStmt.
    def enterIfStmt(self, ctx:ObfuMiniCParser.IfStmtContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#ifStmt.
    def exitIfStmt(self, ctx:ObfuMiniCParser.IfStmtContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#loopStmt.
    def enterLoopStmt(self, ctx:ObfuMiniCParser.LoopStmtContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#loopStmt.
    def exitLoopStmt(self, ctx:ObfuMiniCParser.LoopStmtContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#returnStmt.
    def enterReturnStmt(self, ctx:ObfuMiniCParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#returnStmt.
    def exitReturnStmt(self, ctx:ObfuMiniCParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#ioStmt.
    def enterIoStmt(self, ctx:ObfuMiniCParser.IoStmtContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#ioStmt.
    def exitIoStmt(self, ctx:ObfuMiniCParser.IoStmtContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#expr.
    def enterExpr(self, ctx:ObfuMiniCParser.ExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#expr.
    def exitExpr(self, ctx:ObfuMiniCParser.ExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#assignExpr.
    def enterAssignExpr(self, ctx:ObfuMiniCParser.AssignExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#assignExpr.
    def exitAssignExpr(self, ctx:ObfuMiniCParser.AssignExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#logicOrExpr.
    def enterLogicOrExpr(self, ctx:ObfuMiniCParser.LogicOrExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#logicOrExpr.
    def exitLogicOrExpr(self, ctx:ObfuMiniCParser.LogicOrExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#logicAndExpr.
    def enterLogicAndExpr(self, ctx:ObfuMiniCParser.LogicAndExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#logicAndExpr.
    def exitLogicAndExpr(self, ctx:ObfuMiniCParser.LogicAndExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#equalityExpr.
    def enterEqualityExpr(self, ctx:ObfuMiniCParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#equalityExpr.
    def exitEqualityExpr(self, ctx:ObfuMiniCParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#relationalExpr.
    def enterRelationalExpr(self, ctx:ObfuMiniCParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#relationalExpr.
    def exitRelationalExpr(self, ctx:ObfuMiniCParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#addExpr.
    def enterAddExpr(self, ctx:ObfuMiniCParser.AddExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#addExpr.
    def exitAddExpr(self, ctx:ObfuMiniCParser.AddExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#mulExpr.
    def enterMulExpr(self, ctx:ObfuMiniCParser.MulExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#mulExpr.
    def exitMulExpr(self, ctx:ObfuMiniCParser.MulExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#unaryExpr.
    def enterUnaryExpr(self, ctx:ObfuMiniCParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#unaryExpr.
    def exitUnaryExpr(self, ctx:ObfuMiniCParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:ObfuMiniCParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:ObfuMiniCParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by ObfuMiniCParser#argList.
    def enterArgList(self, ctx:ObfuMiniCParser.ArgListContext):
        pass

    # Exit a parse tree produced by ObfuMiniCParser#argList.
    def exitArgList(self, ctx:ObfuMiniCParser.ArgListContext):
        pass



del ObfuMiniCParser