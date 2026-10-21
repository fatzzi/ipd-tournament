# Loads the class gallery (local-only/strategies.json) through the real app's safety
# check and sandbox, so classmates' code runs exactly as it would on the website.
import os, sys, json, ast, math

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', 'local-only', 'ipd-app')
GALLERY = os.path.join(HERE, '..', 'local-only', 'strategies.json')
sys.path.insert(0, APP)

from core_simulation import extract_strategy_func, ALLOWED_IMPORTS
from n_player_simulation import call_strategy

# Pull is_safe_code (and its helpers) out of app.py without importing Flask.
ns = {'ast': ast, 'math': math, 'ALLOWED_IMPORTS': ALLOWED_IMPORTS,
      'MAX_STRATEGY_CODE_BYTES': 20000, 'MAX_LITERAL_INT_DIGITS': 100,
      'MAX_LITERAL_STR_LEN': 10 ** 6, 'MAX_SEQ_MULTIPLY': 10 ** 6, 'MAX_POW_RESULT_DIGITS': 10 ** 6}
_want = {'is_safe_code', '_static_int', '_is_sequence_literal', '_pow_result_digits', '_oversized_literal_arg'}
for _node in ast.parse(open(os.path.join(APP, 'app.py'), encoding='utf-8').read()).body:
    if isinstance(_node, ast.Assign) and any(getattr(t, 'id', '').startswith('_FORMAT') for t in _node.targets):
        exec(compile(ast.Module([_node], []), 'app.py', 'exec'), ns)
    if isinstance(_node, ast.FunctionDef) and _node.name in _want:
        exec(compile(ast.Module([_node], []), 'app.py', 'exec'), ns)
is_safe_code = ns['is_safe_code']


def load_hub(path=GALLERY):
    d = json.load(open(path, encoding='utf-8'))
    d = d.get('strategies', d) if isinstance(d, dict) else d
    out = {}
    for s in d:
        if s['id'].startswith('tc'):     # "tournament" copies duplicate a bot entry
            continue
        ok, err = is_safe_code(s['code'])
        if not ok:
            print('skipping unsafe', s['name'], err)
            continue
        f = extract_strategy_func(s['code'], seed=1)
        out[s['name']] = (lambda f: lambda l, m, o, meta: call_strategy(f, l, m, o, meta))(f)
    return out
