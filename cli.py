import argparse
import os
import subprocess
from antlr4 import *
from obfuscator.parser.ObfuMiniCLexer import ObfuMiniCLexer
from obfuscator.parser.ObfuMiniCParser import ObfuMiniCParser
from obfuscator.ast_builder import ASTBuilder
from obfuscator.code_generator import CodeGenerator
from obfuscator.name_obfuscator import NameObfuscator
from obfuscator.deadcode import DeadCodeInserter
from obfuscator.expression_transform import ExpressionTransformer
from obfuscator.control_flattening import ControlFlowFlattener
from obfuscator.inliner import FunctionInliner


def run_pipeline(input_path, output_path, stages, check_runtime=False):
    # Step 1: Parse input file
    input_stream = FileStream(input_path)
    lexer = ObfuMiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ObfuMiniCParser(stream)
    tree = parser.compilationUnit()

    # Step 2: Build AST
    ast = ASTBuilder().visit(tree)

    # Step 3: Apply transformations
    if "rename" in stages:
        NameObfuscator().obfuscate(ast)
    if "dead" in stages:
        DeadCodeInserter().insert(ast)
    if "expr" in stages:
        ExpressionTransformer().transform(ast)
    if "flatten" in stages:
        ControlFlowFlattener().flatten(ast)
    if "inline" in stages:
        FunctionInliner(ast).inline()

    # Step 4: Generate code
    code = CodeGenerator().generate(ast)

    # Step 5: Output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(code)
    print(f"[✓] Obfuscated code saved to {output_path}")

    # Step 6: Runtime behavior check
    if check_runtime:
        run_and_compare(input_path, output_path)


def run_and_compare(original_path, obfuscated_path):
    def compile_and_run(src_path):
        bin_path = src_path.replace(".mc", ".out")
        compile_cmd = ["gcc", src_path, "-o", bin_path]
        try:
            subprocess.run(
                compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            result = subprocess.run(
                [bin_path], check=True, capture_output=True, text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"[✗] Error: {e.stderr}")
            return None

    print("[*] Checking runtime equivalence...")
    orig_output = compile_and_run(original_path)
    obfus_output = compile_and_run(obfuscated_path)

    if orig_output == obfus_output:
        print("[✓] Runtime outputs match. Equivalence confirmed.")
    else:
        print("[✗] Output mismatch!")
        print("Original:", orig_output)
        print("Obfuscated:", obfus_output)


def main():
    parser = argparse.ArgumentParser(description="Mini-C Obfuscator CLI")
    parser.add_argument("input", help="Path to input .mc file")
    parser.add_argument(
        "-o",
        "--output",
        default="output/output.mc",
        help="Output file path (default: output/output.mc)",
    )
    parser.add_argument("--rename", action="store_true", help="Apply variable renaming")
    parser.add_argument("--dead", action="store_true", help="Insert dead code")
    parser.add_argument("--expr", action="store_true", help="Transform expressions")
    parser.add_argument(
        "--flatten", action="store_true", help="Apply control flow flattening"
    )
    parser.add_argument("--inline", action="store_true", help="Inline simple functions")
    parser.add_argument("--all", action="store_true", help="Apply all transformations")
    parser.add_argument(
        "--check", action="store_true", help="Run GCC equivalence check"
    )

    args = parser.parse_args()

    selected_stages = []
    if args.all:
        selected_stages = ["rename", "dead", "expr", "flatten", "inline"]
    else:
        if args.rename:
            selected_stages.append("rename")
        if args.dead:
            selected_stages.append("dead")
        if args.expr:
            selected_stages.append("expr")
        if args.flatten:
            selected_stages.append("flatten")
        if args.inline:
            selected_stages.append("inline")

    run_pipeline(args.input, args.output, selected_stages, args.check)


if __name__ == "__main__":
    main()
