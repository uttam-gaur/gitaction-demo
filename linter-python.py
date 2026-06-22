#!/usr/bin/env python3
"""mini_lint.py - tiny pure-Python linter. Usage: python mini_lint.py file.py"""

import ast
import sys


def check(path):
    src = open(path, encoding="utf-8").read()
    issues = []

    for i, line in enumerate(src.splitlines(), 1):
        if len(line) > 100:
            issues.append(f"{path}:{i}: line too long ({len(line)} > 100)")
        if line != line.rstrip():
            issues.append(f"{path}:{i}: trailing whitespace")

    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        return [f"{path}:{e.lineno}: SyntaxError: {e.msg}"]

    imported, used = {}, set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported[a.asname or a.name.split(".")[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                if a.name != "*":
                    imported[a.asname or a.name] = node.lineno
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
        elif isinstance(node, ast.FunctionDef):
            n = len(node.args.args)
            if n > 6:
                issues.append(f"{path}:{node.lineno}: '{node.name}' has too many args ({n})")
            for d in node.args.defaults:
                if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    issues.append(f"{path}:{node.lineno}: '{node.name}' has mutable default arg")
        elif isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(f"{path}:{node.lineno}: bare 'except:' clause")
        elif isinstance(node, ast.Compare):
            for op, c in zip(node.ops, node.comparators):
                if isinstance(op, (ast.Eq, ast.NotEq)) and isinstance(c, ast.Constant) and c.value is None:
                    issues.append(f"{path}:{node.lineno}: use 'is'/'is not' with None, not =='/'!='")

    for name, lineno in imported.items():
        if name not in used:
            issues.append(f"{path}:{lineno}: '{name}' imported but never used")

    return issues


if __name__ == "__main__":
    all_issues = [i for f in sys.argv[1:] for i in check(f)]
    print("\n".join(all_issues) or "No issues found.")
    sys.exit(1 if all_issues else 0)
