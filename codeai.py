#!/usr/bin/env python3
"""
Console -> MyLibrary converter, compatible with Python 3.7+.

Usage:
    python converter.py input_script.py output_fg.py

Notes:
- For Python >= 3.9 this uses ast.unparse.
- For Python < 3.9 it will try astunparse, then astor. Install one with:
    pip install astunparse
  or
    pip install astor
"""

import ast
import sys
import json
from typing import List, Tuple

# Provide a compatible 'unparse' function for Python 3.7+
try:
    # Python 3.9+
    unparse = ast.unparse  # type: ignore
except AttributeError:
    try:
        import astunparse  # type: ignore

        def unparse(node):
            return astunparse.unparse(node)
    except Exception:
        try:
            import astor  # type: ignore

            def unparse(node):
                return astor.to_source(node)
        except Exception:
            raise RuntimeError(
                "No AST unparser available. For Python <3.9 install 'astunparse' or 'astor' (pip install astunparse)."
            )


class InputAndPrintTransformer(ast.NodeTransformer):
    """
    Replaces input(...) calls with self.inputs[self.inputs_number[N]].get()
    and replaces print(...) with self.print(...).
    Keeps a list of prompts in order of discovery.
    """

    def __init__(self):
        super().__init__()
        self.input_prompts: List[str] = []
        # count of input occurrences, used to generate indices (1-based to match your example)
        self._counter = 0

    def _make_input_node(self, prompt_node: ast.AST) -> ast.AST:
        # record prompt if it's a string literal, otherwise make generic prompt
        prompt = ""
        if isinstance(prompt_node, ast.Constant) and isinstance(prompt_node.value, str):
            prompt = prompt_node.value
        else:
            # if it's not a literal, try to unparse it; fallback to empty string
            try:
                prompt = unparse(prompt_node).strip()
            except Exception:
                prompt = ""
        self._counter += 1
        idx = self._counter
        self.input_prompts.append(prompt)
        # build AST from text: self.inputs[self.inputs_number[idx]].get()
        expr_code = f"self.inputs[self.inputs_number[{idx}]].get()"
        node = ast.parse(expr_code, mode="eval").body
        return node

    def visit_Call(self, node: ast.Call) -> ast.AST:
        # First, recursively transform inner calls/args
        self.generic_visit(node)

        # Handle input(...)
        if isinstance(node.func, ast.Name) and node.func.id == "input":
            if node.args:
                prompt_node = node.args[0]
            else:
                prompt_node = ast.Constant(value="")
            return self._make_input_node(prompt_node)

        # Handle print(...)
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            # rebuild arguments into code via unparse for accuracy
            try:
                args_code = ", ".join(unparse(a).strip() for a in node.args) if node.args else ""
            except Exception:
                args_code = ""
            new_expr = f"self.print({args_code})"
            return ast.parse(new_expr, mode="eval").body

        return node


def transform_source_to_my_library(source: str, example_desc: str = "Converted by converter") -> Tuple[str, List[str]]:
    """
    Parses python source, replaces input/print, returns final module code string
    (ready content for a file using ForExample.MyLibrary) and list of prompts.
    """
    tree = ast.parse(source)
    transformer = InputAndPrintTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    # Unparse transformed user code
    try:
        transformed_code = unparse(new_tree)
    except Exception as e:
        raise RuntimeError(f"Failed to unparse transformed AST: {e}")

    # Build final file content
    header = "from ForExample import MyLibrary\n\n"
    header += f"myapp = MyLibrary(\n    flag=True,\n    example={json.dumps(example_desc)}\n)\n\n"

    # Add myapp.Input lines based on collected prompts
    input_lines = ""
    for i, prompt in enumerate(transformer.input_prompts, start=1):
        p = prompt if prompt is not None else ""
        input_lines += f"myapp.Input({json.dumps(p)}, number={i})\n"
    if input_lines:
        input_lines += "\n"

    # Prepare user_code as a triple-quoted string literal safely via json.dumps
    user_code_literal = json.dumps(transformed_code, ensure_ascii=False)
    body = (
        header
        + input_lines
        + f"user_code = {user_code_literal}\n\n"
        + "myapp.main_code(user_code)\n\n"
        + "myapp.run()\n"
    )

    return body, transformer.input_prompts


def main(argv):
    if len(argv) != 3:
        print("Usage: python converter.py input_script.py output_fg.py")
        return 2
    infile, outfile = argv[1], argv[2]
    with open(infile, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        out_code, prompts = transform_source_to_my_library(src, example_desc=f"Converted from {infile}")
    except Exception as e:
        print("Error during transformation:", e)
        return 1

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(out_code)

    print(f"Wrote converted file to {outfile}")
    if prompts:
        print("Detected input prompts:")
        for i, p in enumerate(prompts, start=1):
            print(f"  {i}. {p}")
    else:
        print("No input() calls detected.")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
