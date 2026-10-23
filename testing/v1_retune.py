# Sprint 1 1v1 retune for POINTS-ONLY ranking (weights points=1.0).
#
# Fast + exact: the opponent-vs-opponent matches don't change when only our entry (ME)
# changes, so they are played once per seed and cached; each variant then only plays ME
# against every opponent and adds that match's contribution to the opponents' totals.
# Ranking metric = points_percentage = (total raw points / total moves) / max payoff,
# exactly as app.py computes it (verified identical to the real engine).
#
#   python testing/v1_retune.py            # hidden-code snapshot field only, 8 seeds
#   python testing/v1_retune.py +base      # also add classic baselines to the pool (anti-overfit)
#   python testing/v1_retune.py +base 16   # ... over 16 seeds
import sys, random, statistics
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
from hubfield import load_hub
from sim import game, MATS, MODES
import field as F

MAT = MATS['S1']
MX = max(v[0] for v in MAT.values())
TI = {'weights': {'points': 1}, 'payoff_matrix': MAT, 'format': '2-player',
      'n_players': 2, 'payoff_model': 'standard'}
BOTS = {'multiplicative_update', "Claude's_strategy", 'multiplicative_update_merciful',
        'probabilistic_expectation', 'Salman', "Hijab's strategy"}
SRC = open(r'C:\Users\fxtim\Desktop\ipd-tournament\strategies\strategy.py', encoding='utf-8').read()

def mk(**rep):
    s = SRC
    for a, b in rep.items():
        assert a in s, 'missing: ' + a
        s = s.replace(a, b)
    g = {}
    exec(s, g)
    return g['sentinel']

# strategy.py now defaults to ENDGAME_1V1 = 1 and GEN = 0.2 (round-based). Compare the chosen
# config against turning generosity off/up and reverting the endgame, with the clean mechanism.
def gen(x): return {'GEN = 0.2': f'GEN = {x}'}
VARIANTS = {
    'chosen(e1 gen.2)': {},
    'gen off'         : gen(0.0),
    'gen.15'          : gen(0.15),
    'gen.3'           : gen(0.3),
    'end2 gen.2'      : {'ENDGAME_1V1 = 1': 'ENDGAME_1V1 = 2'},
    'OLD end7 gen0'   : {'ENDGAME_1V1 = 1': 'ENDGAME_1V1 = 7', 'GEN = 0.2': 'GEN = 0.0'},
}

addbase = '+base' in sys.argv
nums = [a for a in sys.argv[1:] if a.isdigit()]
NSEED = int(nums[0]) if nums else 8
compiled = {vn: mk(**rep) for vn, rep in VARIANTS.items()}
agg = {vn: {'pp': [], 'rank': []} for vn in VARIANTS}

def play(fa, fb, seed):
    """Total raw points (a, b) and total moves over the 4 modes at this seed."""
    ra = rb = mv = 0
    for mi, mode in enumerate(MODES):
        _, _, pa, pb, _, _, r = game(fa, fb, MAT, mode, R, seed + mi, TI)
        ra += pa; rb += pb; mv += r
    return ra, rb, mv

for seed in range(1, NSEED + 1):
    hub = load_hub(); hub.pop('yay', None)
    if addbase:
        for bn, bf in F.FIELD.items():
            hub.setdefault('B_' + bn, bf)
    names = sorted(hub)
    funcs = [hub[n] for n in names]
    R = random.Random(seed).randint(100, 300)
    base_raw = {n: 0 for n in names}
    base_mv = {n: 0 for n in names}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ra, rb, mv = play(funcs[i], funcs[j], seed + (i * 1000 + j) * 7 + 500000)
            base_raw[names[i]] += ra; base_mv[names[i]] += mv
            base_raw[names[j]] += rb; base_mv[names[j]] += mv
    for vn, me in compiled.items():
        raw = dict(base_raw); mv = dict(base_mv); me_raw = me_mv = 0
        for k, n in enumerate(names):
            a, b, m = play(me, funcs[k], seed + k * 1000)
            me_raw += a; me_mv += m
            raw[n] += b; mv[n] += m
        pp = {n: raw[n] / mv[n] / MX for n in names}
        pp['ME'] = me_raw / me_mv / MX
        order = [n for n in sorted(pp, key=lambda n: -pp[n]) if n not in BOTS]
        agg[vn]['pp'].append(pp['ME'])
        agg[vn]['rank'].append(order.index('ME') + 1)

print(f'== 1v1 POINTS-ONLY  ({NSEED} seeds, field: {"snapshot+baselines" if addbase else "snapshot only"})')
print(f'{"variant":14s}  {"mean pts%":>9s}  {"top3":>6s}  {"meanRank":>8s}  ranks')
for vn in sorted(VARIANTS, key=lambda v: -statistics.mean(agg[v]['pp'])):
    r = agg[vn]['rank']
    print(f'{vn:14s}  {statistics.mean(agg[vn]["pp"])*100:9.3f}  {sum(x<=3 for x in r):>3d}/{len(r):<2d}  '
          f'{statistics.mean(r):8.2f}  {r}', flush=True)
