from deobfuscator.ast_builder import ASTBuilder
from deobfuscator.code_generator import CodeGenerator
from antlr4 import FileStream, CommonTokenStream
from deobfuscator.parser.ObfuMiniCLexer import ObfuMiniCLexer
from deobfuscator.parser.ObfuMiniCParser import ObfuMiniCParser

def main():
    # 1. خواندن و پارس کردن ورودی
    input_stream = FileStream("input/input.mc")
    lexer = ObfuMiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ObfuMiniCParser(stream)
    tree = parser.compilationUnit()

    # 2. ساختن AST
    ast_builder = ASTBuilder()
    ast = ast_builder.visit(tree)

    # <<<<<<<<< در این قسمت فعلاً هیچ تکنیک ساده‌سازی اعمال نمی‌کنیم >>>>>>>>>

    # 3. تولید کد خروجی از روی همان AST بدون تغییر
    code_gen = CodeGenerator()
    output_code = code_gen.generate(ast)

    # 4. ذخیره خروجی
    with open("output/cleaned.mc", "w") as f:
        f.write(output_code)
    
    print("Initial test finished. Check output/cleaned.mc")

if __name__ == '__main__':
    main()