# N-Player top-3 rate against the real gallery for each round's settings.
import sys, statistics
from hubfield import load_hub
from sim import tournament_np
src = open(sys.argv[1]).read()
def ld(**rep):
    s = src
    for a, b in rep.items():
        assert a in s, a; s = s.replace(a, b)
    g = {}; exec(s, g); return g['sentinel']
V = {'current': ld(), 'alwaysD(BIG_GROUP=2)': ld(**{'BIG_GROUP = 7 ': 'BIG_GROUP = 2 '})}
for mk, (b, gs) in (('S1', (0.4, 5)), ('S2', (0.3, 5)), ('F', (0.25, 8))):
    for vn, v in V.items():
        ranks = []
        for seed in range(1, 61):
            s = load_hub(); s['ME'] = v
            pts = tournament_np(s, b, gs, seed=seed, modes=['standard', 'discounted', 'stochastic', 'random'])
            o = sorted(pts, key=lambda n: -pts[n]); ranks.append(o.index('ME') + 1)
        print(f'{mk} {vn:22s} top3 {sum(r <= 3 for r in ranks)}/60  mean rank {statistics.mean(ranks):.1f}/{len(s)}', flush=True)
