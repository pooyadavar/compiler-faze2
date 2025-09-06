from deobfuscator.ast_builder import ASTBuilder
from deobfuscator.code_generator import CodeGenerator
from antlr4 import FileStream, CommonTokenStream
from deobfuscator.parser.ObfuMiniCLexer import ObfuMiniCLexer
from deobfuscator.parser.ObfuMiniCParser import ObfuMiniCParser
from deobfuscator.techniques.expression_simplifier import ExpressionSimplifier 
from deobfuscator.techniques.control_flow_simplifier import ControlFlowSimplifier 

def main():

    input_stream = FileStream("input/input.mc")
    lexer = ObfuMiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ObfuMiniCParser(stream)
    tree = parser.compilationUnit()

    ast_builder = ASTBuilder()
    ast = ast_builder.visit(tree)


    print("\nApplying Expression Simplification...")
    simplifier = ExpressionSimplifier()
    simplified_ast = simplifier.visit(ast)
    print("Simplification finished.")



    print("\nApplying Control Flow Simplification...")
    cf_simplifier = ControlFlowSimplifier()
    final_ast = cf_simplifier.visit(simplified_ast)
    print("Simplification finished.")

    code_gen = CodeGenerator()
    output_code = code_gen.generate(ast)


    with open("output/cleaned.mc", "w") as f:
        f.write(output_code)
    
    print("Initial test finished. Check output/cleaned.mc")

if __name__ == '__main__':
    main()