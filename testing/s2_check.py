# Submission check against the real v1.4.0 engine: safety screen, URL size, and one run of
# each game (1v1 vs TFT in all 4 modes, an N-Player group, the OS sim) under the line cap.
import os, sys, ast, math, random
from urllib.parse import quote
APP = r'C:/Users/fxtim/AppData/Local/Temp/v140/COMPUTATION-NOT-FOUND-ipd-app-cb47fd6'
sys.path.insert(0, APP)
from core_simulation import extract_strategy_func, ALLOWED_IMPORTS, run_full_simulation
from n_player_simulation import game_n
from payoff_models import PublicGoodsPayoff
from instruction_limit import run_with_limit
ns = {'ast': ast, 'math': math, 'ALLOWED_IMPORTS': ALLOWED_IMPORTS,
      'MAX_STRATEGY_CODE_BYTES': 20000, 'MAX_LITERAL_INT_DIGITS': 100,
      'MAX_LITERAL_STR_LEN': 10 ** 6, 'MAX_SEQ_MULTIPLY': 10 ** 6, 'MAX_POW_RESULT_DIGITS': 10 ** 6}
want = {'is_safe_code', '_static_int', '_is_sequence_literal', '_pow_result_digits', '_oversized_literal_arg'}
for node in ast.parse(open(os.path.join(APP, 'app.py'), encoding='utf-8').read()).body:
    if isinstance(node, ast.Assign) and any(getattr(t, 'id', '').startswith('_') for t in node.targets):
        try: exec(compile(ast.Module([node], []), 'app.py', 'exec'), ns)
        except Exception: pass
    if isinstance(node, ast.FunctionDef) and node.name in want:
        exec(compile(ast.Module([node], []), 'app.py', 'exec'), ns)
if __name__ == '__main__':
    code = open('strategies/submit.py', encoding='utf-8').read()
    print('bytes', len(code), 'encoded', len(quote(code)), 'safe', ns['is_safe_code'](code))
    me = extract_strategy_func(code, seed=1)
    cap = lambda f: (lambda *a: run_with_limit(f, *a))
    tft = lambda l, m, o, meta: l[0] if l else 'C'
    maj = lambda l, m, o, meta: 'C' if not l or l.count('C') * 2 >= len(l) else 'D'
    pg = PublicGoodsPayoff(b=0.3, c=1)
    ti = {'weights': {'points': 0.5, 'cooperation': 0.3, 'win_rate': 0.2}, 'rounds': 200,
          'modes': ['standard', 'discounted', 'stochastic', 'random']}
    for mode in ti['modes']:
        r = game_n([cap(me), maj, maj, maj, tft], 200, pg, seed=5, tournament_info=dict(ti, mode=mode), mode=mode, fixed_random_rounds=250)
        print('NP', mode, r.get('error'), {k: round(v, 1) for k, v in r['total_points_by_player'].items()}, r['coop_counts_by_player'][0], r['rounds_played'])
    o = run_full_simulation([{'name': 'ME', 'code': code}], num_cores=8, seed=29257, scheduler='priority', runs=2, num_processes=100)
    print('OS', o['errors'], o['strategies'].get('ME', {}).get('avg', {}).get('avg_response'))
