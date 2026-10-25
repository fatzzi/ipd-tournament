# Sprint 2 1v1: weighted score (points 50, coop 30, win 20) with the 4/0/6/2 table.
# The field is drawn at random from textbook strategy families (no classmate code), many
# times over, so a variant only wins here if it wins against many different populations.
import sys, os, random, re
END = float(os.environ.get('ENDSCALE', '1'))  # stretch every family's endgame length (stress test)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim import tournament_1v1, MATS
W = {'points': 0.5, 'cooperation': 0.3, 'win_rate': 0.2}
MAT = MATS['S2']

def tft_end(k, start='C', forgive=0.0, contrite=False):
    k = round(k * END)
    def f(l, m, o, meta):
        r = meta['round']
        if k and 200 - k <= r < 200: return 'D'
        if not l: return start
        if l[0] == 'C': return 'C'
        if contrite and len(m) >= 2 and m[-2] == 'D' and o[0][-2] == 'C': return 'C'
        if forgive and meta['rng'].random() < forgive: return 'C'
        return 'D'
    return f
def grim_end(k):
    k = round(k * END)
    def f(l, m, o, meta):
        if k and 200 - k <= meta['round'] < 200: return 'D'
        return 'D' if 'D' in o[0] else 'C'
    return f
def pavlov_end(k):
    def f(l, m, o, meta):
        if k and 200 - k <= meta['round'] < 200: return 'D'
        if not l: return 'C'
        return m[-1] if l[0] == 'C' else ('D' if m[-1] == 'C' else 'C')
    return f
def tf2t(l, m, o, meta):
    h = o[0]; return 'D' if len(h) >= 2 and h[-1] == h[-2] == 'D' else 'C'
def alld(l, m, o, meta): return 'D'
def allc(l, m, o, meta): return 'C'
def rnd(p):
    def f(l, m, o, meta): return 'C' if meta['rng'].random() < p else 'D'
    return f
def prober(l, m, o, meta):
    r = meta['round']
    if r < 4: return 'CDCC'[r]
    if 'D' not in o[0][1:4]: return 'D'
    return l[0]
def joss(p):  # TFT that sneaks a defection now and then
    def f(l, m, o, meta):
        if not l: return 'C'
        if l[0] == 'D': return 'D'
        return 'D' if meta['rng'].random() < p else 'C'
    return f
def never_trail(k):  # TFT, but keeps defecting while behind in the match
    k = round(k * END)
    def f(l, m, o, meta):
        r = meta['round']
        if k and 200 - k <= r < 200: return 'D'
        if not l: return 'C'
        t = MAT
        if sum(t[a + b][0] - t[a + b][1] for a, b in zip(m, o[0])) < 0: return 'D'
        return l[0]
    return f
def alternator(l, m, o, meta): return 'CD'[meta['round'] % 2]

FAMILIES = {
    'TFT': lambda rg: tft_end(rg.choice([0, 0, 1, 1, 2, 3, 5])),
    'GTFT': lambda rg: tft_end(rg.choice([0, 1, 2]), forgive=0.1),
    'CTFT': lambda rg: tft_end(rg.choice([0, 1, 1, 2, 3, 4, 6, 8]), contrite=True),
    'STFT': lambda rg: tft_end(rg.choice([0, 1]), start='D'),
    'Grim': lambda rg: grim_end(rg.choice([0, 1, 2])),
    'Pavlov': lambda rg: pavlov_end(rg.choice([0, 1])),
    'TF2T': lambda rg: tf2t, 'AllD': lambda rg: alld, 'AllC': lambda rg: allc,
    'Rand': lambda rg: rnd(rg.choice([0.3, 0.5, 0.7])), 'Prober': lambda rg: prober,
    'Joss': lambda rg: joss(rg.choice([0.05, 0.1])), 'NeverTrail': lambda rg: never_trail(rg.choice([1, 2, 3, 5, 7])),
    'Alt': lambda rg: alternator,
}
# Rough share of each family in a class of Claude-assisted students (mostly reciprocators).
SHARE = {'TFT': 6, 'GTFT': 3, 'CTFT': 8, 'STFT': 1, 'Grim': 3, 'Pavlov': 2, 'TF2T': 2, 'AllD': 2, 'AllC': 1,
         'Rand': 1, 'Prober': 1, 'Joss': 1, 'NeverTrail': 5, 'Alt': 1}

def field(seed, size=30):
    rg = random.Random(seed); fams = list(SHARE)
    out = {}
    for i in range(size):
        fam = rg.choices(fams, [SHARE[f] for f in fams])[0]
        out[f'{fam}_{i}'] = FAMILIES[fam](rg)
    return out

def load(path, **subs):
    src = open(path, encoding='utf-8').read()
    for k, v in subs.items():
        src, n = re.subn(rf'^(\s*{k}\s*=\s*)[^#\n]+', rf'\g<1>{v} ', src, flags=re.M)
        assert n == 1, k
    g = {}; exec(src, g); return g['sentinel']

if __name__ == '__main__':
    path = 'strategies/strategy.py'
    variants = {'weight-aware (new)': {}}
    HEAD = os.environ.get('HEAD_COPY')
    nseeds = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    if HEAD: variants['committed (d53091e)'] = 'head'
    stats = {v: [] for v in variants}
    for sd in range(nseeds):
        base = field(sd)
        for v, subs in variants.items():
            f = dict(base); f['ME'] = load(path, **subs) if subs != 'head' else load(HEAD)
            res = tournament_1v1(f, MAT, seed=100 + sd, weights=W)
            order = sorted(res, key=lambda n: -res[n]['weighted'])
            stats[v].append((order.index('ME') + 1, res['ME']['weighted'] * 100, res['ME']['win']))
        print('seed', sd, {v: s[-1][0] for v, s in stats.items()}, flush=True)
    print(f"{'variant':16} mean_rank  top3  wins  score")
    for v, s in stats.items():
        print(f'{v:16} {sum(x[0] for x in s)/len(s):8.2f}  {sum(x[0]<=3 for x in s):3}/{len(s)}  '
              f'{sum(x[2] for x in s)/len(s):.2f}  {sum(x[1] for x in s)/len(s):.2f}')
