# Writes strategies/submit.py: strategies/strategy.py with comments and docstrings removed.
import os, ast

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
src = open(os.path.join(ROOT, 'strategies', 'strategy.py'), encoding='utf-8').read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.Module)) and node.body \
            and isinstance(node.body[0], ast.Expr) \
            and isinstance(getattr(node.body[0], 'value', None), ast.Constant) \
            and isinstance(node.body[0].value.value, str):
        node.body = node.body[1:]
with open(os.path.join(ROOT, 'strategies', 'submit.py'), 'w', encoding='utf-8') as f:
    f.write(ast.unparse(tree) + '\n')
print('wrote strategies/submit.py')
