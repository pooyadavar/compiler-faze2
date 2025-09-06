grammar ObfuMiniC;

compilationUnit : (funcDef | varDecl)* EOF ;

funcDef     : type ID '(' paramList? ')' blockStmt ;

paramList   : param (',' param)* ;
param       : type ID ;

varDecl     : type initList ';' ;
initList    : init (',' init)* ;
init        : ID ('=' expr)?;

type : INT | CHAR_TOK | BOOL_TOK ;

blockStmt   : '{' (varDecl | stmt)* '}' ;

stmt
    : exprStmt
    | blockStmt
    | ifStmt
    | loopStmt
    | returnStmt
    | ioStmt
    | switchStmt   ;

switchStmt
    : 'switch' '(' expr ')' '{' switchBlock* '}'
    ;

switchBlock
    : caseBlock
    | defaultBlock
    ;

caseBlock
    : 'case' literal ':' stmt*
    ;

defaultBlock
    : 'default' ':' stmt*
    ;

literal
    : NUMBER
    | CHAR
    | BOOL
    ;

exprStmt    : expr? ';' ;

ifStmt      : 'if' '(' expr ')' stmt ('else' stmt)? ;

loopStmt
    : WHILE '(' expr ')' stmt
    | FOR '(' expr? ';' expr? ';' expr? ')' stmt ;

returnStmt  : 'return' expr? ';' ;

ioStmt
    : PRINTF '(' STRING (',' expr)* ')' ';'
    | SCANF  '(' STRING (',' '&'? ID)* ')' ';' ;

expr
    : assignExpr ;

assignExpr
    : logicOrExpr ('=' assignExpr)? ;

logicOrExpr
    : logicAndExpr ('||' logicAndExpr)* ;

logicAndExpr
    : equalityExpr ('&&' equalityExpr)* ;

equalityExpr
    : relationalExpr (('==' | '!=') relationalExpr)* ;

relationalExpr
    : addExpr (('<' | '<=' | '>' | '>=') addExpr)* ;

addExpr
    : mulExpr (('+' | '-') mulExpr)* ;

mulExpr
    : unaryExpr (('*' | '/' | '%') unaryExpr)* ;

unaryExpr
    : ('+' | '-' | '!') unaryExpr
    | primaryExpr ;

primaryExpr
    : ID LPAREN argList? RPAREN     
    | ID
    | NUMBER
    | CHAR
    | BOOL
    | STRING 
    | '(' expr ')' ;

argList     : expr (',' expr)* ;

// ----------------------- LEXER RULES -----------------------

BOOL        : 'true' | 'false' ;
CHAR        : '\'' . '\'' ;
STRING      : '"' (~["\\] | '\\' .)* '"' ;

INT         : 'int' ;
CHAR_TOK    : 'char' ;
BOOL_TOK    : 'bool' ;
PRINTF      : 'printf' ;
SCANF       : 'scanf' ;
WHILE       : 'while' ;
FOR         : 'for' ;
IF          : 'if' ;
ELSE        : 'else' ;
RETURN      : 'return' ;

// SYMBOLES
LPAREN      : '(' ;
RPAREN      : ')' ;
LBRACE      : '{' ;
RBRACE      : '}' ;
SEMI        : ';' ;
COMMA       : ',' ;

NUMBER      : [0-9]+ ;
ID          : [a-zA-Z_][a-zA-Z0-9_]* ;

WS          : [ \t\r\n]+ -> skip ;
LINE_COMMENT: '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT: '/*' .*? '*/' -> skip ;
