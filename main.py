from deobfuscator.ast_builder import ASTBuilder
from deobfuscator.code_generator import CodeGenerator
from antlr4 import FileStream, CommonTokenStream
from deobfuscator.parser.ObfuMiniCLexer import ObfuMiniCLexer
from deobfuscator.parser.ObfuMiniCParser import ObfuMiniCParser
from deobfuscator.techniques.expression_simplifier import ExpressionSimplifier 
from deobfuscator.techniques.control_flow_simplifier import ControlFlowSimplifier 
from deobfuscator.techniques.dead_code_remover import DeadCodeRemover
from deobfuscator.techniques.inline_reconstructor import InlineReconstructor
from deobfuscator.techniques.name_recoverer import SemanticNameRecoverer
from deobfuscator.ast_builder import ASTBuilder
from deobfuscator.code_generator import CodeGenerator
def main():
    # --- Parse input file ---
    input_stream = FileStream("input/input.mc")
    lexer = ObfuMiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ObfuMiniCParser(stream)
    tree = parser.compilationUnit()

    # --- Build AST ---
    ast_builder = ASTBuilder()
    prog = ast_builder.visit(tree)

    print("[deobfuscator] removing dead code...")
    dc = DeadCodeRemover()
    dc.remove(prog)

    print("[deobfuscator] simplifying expressions...")
    es = ExpressionSimplifier()
    es.simplify(prog)

    print("[deobfuscator] simplifying control flow...")
    cf_simplifier = ControlFlowSimplifier()
    cf_simplifier.visit(prog)

    print("[deobfuscator] reconstructing inlined functions...")
    ic = InlineReconstructor()
    ic.reconstruct(prog)

    print("[deobfuscator] recovering readable names...")
    rn = SemanticNameRecoverer()
    rn.recover(prog)

    # --- Generate code ---
    code_gen = CodeGenerator()
    output_code = code_gen.generate(prog)

    with open("output/cleaned.mc", "w") as f:
        f.write(output_code)

    print("Deobfuscation finished. Check output/cleaned.mc")
if __name__ == '__main__':
    main()
