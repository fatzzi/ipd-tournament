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
# The local app hands the code to the website in a URL capped at 7500 characters, so
# use 1-space indents and plain \n line endings (every encoded space costs 3).
out = []
for line in ast.unparse(tree).split('\n'):
    body = line.lstrip(' ')
    out.append(' ' * ((len(line) - len(body)) // 4) + body)
with open(os.path.join(ROOT, 'strategies', 'submit.py'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(out) + '\n')
print('wrote strategies/submit.py')
