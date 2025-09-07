import argparse
import os
import subprocess
from antlr4 import *
from deobfuscator.parser.ObfuMiniCLexer import ObfuMiniCLexer
from deobfuscator.parser.ObfuMiniCParser import ObfuMiniCParser
from deobfuscator.ast_builder import ASTBuilder
from deobfuscator.code_generator import CodeGenerator
from deobfuscator.techniques.dead_code_remover import DeadCodeRemover
from deobfuscator.techniques.expression_simplifier import ExpressionSimplifier
from deobfuscator.techniques.name_recoverer import SemanticNameRecoverer
from deobfuscator.techniques.control_flow_simplifier import ControlFlowSimplifier 
from deobfuscator.techniques.inline_reconstructor import InlineReconstructor


def run_pipeline(input_path, output_path, stages, check_runtime=False):
    # Step 1: Parse input file
    input_stream = FileStream(input_path)
    lexer = ObfuMiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ObfuMiniCParser(stream)
    tree = parser.compilationUnit()

    # Step 2: Build AST
    ast = ASTBuilder().visit(tree)

    # Step 3: Apply deobfuscation stages
    if "dead" in stages:
        DeadCodeRemover().remove(ast)
    if "expr" in stages:
        ExpressionSimplifier().simplify(ast)
    if "rename" in stages:
        SemanticNameRecoverer().recover(ast)
    if "control" in stages:
        ControlFlowSimplifier().visit(ast)
    if "inline" in stages:
        InlineReconstructor().reconstruct(ast)

    # Step 4: Generate clean code
    code = CodeGenerator().generate(ast)

    # Step 5: Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(code)
    print(f"[✓] Deobfuscated code saved to {output_path}")

    # Step 6: Runtime check
    if check_runtime:
        run_and_compare(input_path, output_path)


def run_and_compare(obfus_path, clean_path):
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
    obfus_output = compile_and_run(obfus_path)
    clean_output = compile_and_run(clean_path)

    if obfus_output == clean_output:
        print("[✓] Runtime outputs match. Equivalence confirmed.")
    else:
        print("[✗] Output mismatch!")
        print("Obfuscated:", obfus_output)
        print("Clean:", clean_output)


def main():
    parser = argparse.ArgumentParser(description="Mini-C Deobfuscator CLI")
    parser.add_argument("input", help="Path to obfuscated .mc file")
    parser.add_argument(
        "-o",
        "--output",
        default="output/output_clean.mc",
        help="Output file path (default: output/output_clean.mc)",
    )
    parser.add_argument("--rename", action="store_true", help="Recover variable names")
    parser.add_argument("--dead", action="store_true", help="Remove dead code")
    parser.add_argument("--expr", action="store_true", help="Simplify expressions")
    parser.add_argument("--control", action="store_true", help="Simplify control flow")
    parser.add_argument("--inline", action="store_true", help="Reconstruct inlined functions")
    parser.add_argument("--all", action="store_true", help="Apply all transformations")
    parser.add_argument("--check", action="store_true", help="Run GCC equivalence check")

    args = parser.parse_args()

    selected_stages = []
    if args.all:
        selected_stages = ["dead", "expr", "rename", "control", "inline"]
    else:
        if args.dead: selected_stages.append("dead")
        if args.expr: selected_stages.append("expr")
        if args.rename: selected_stages.append("rename")
        if args.control: selected_stages.append("control")
        if args.inline: selected_stages.append("inline")

    run_pipeline(args.input, args.output, selected_stages, args.check)


if __name__ == "__main__":
    main()
