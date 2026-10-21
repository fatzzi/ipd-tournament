# 1v1 and N-Player against the real class gallery, for strategy variants.
# usage: python testing/eval_real.py strategies/strategy.py [S1|S2|F]
import sys, statistics
from hubfield import load_hub
from sim import tournament_1v1, tournament_np, MATS

src = open(sys.argv[1]).read()
mk = sys.argv[2] if len(sys.argv) > 2 else 'S1'
PG = {'S1': (0.4, 5), 'S2': (0.3, 5), 'F': (0.25, 8)}[mk]


def ld(**rep):
    s = src
    for a, b in rep.items():
        assert a in s, a
        s = s.replace(a, b)
    g = {}
    exec(s, g)
    return g['sentinel']


V1 = {f'end{d}': ld(**{'ENDGAME_1V1 = 3': f'ENDGAME_1V1 = {d}'}) for d in (3, 5, 6, 7)}
print(f'== 1v1 {mk}')
for wk, w in (('points', {'points': 1}), ('equal', {'win_rate': 1, 'cooperation': 1, 'points': 1}),
              ('win', {'win_rate': 1})):
    line = []
    for vn, v in V1.items():
        ranks = []
        for seed in (1, 2, 3):
            s = load_hub()
            s['ME'] = v
            out = tournament_1v1(s, MATS[mk], seed=seed, weights=w)
            o = sorted(out, key=lambda n: -out[n]['weighted'])
            ranks.append(o.index('ME') + 1)
        line.append(f'{vn} {ranks}')
    print(f'{wk:7s}', ' | '.join(line), '| top3 last:', o[:3], flush=True)

print(f'== N-Player {mk} (b={PG[0]}, groups of {PG[1]}), top-3 hits over 30 group shuffles')
VN = {'current': ld(), 'always_D': (lambda l, m, o, meta: 'D'),
      'no_probe': ld(**{'PROBE_NP = 2': 'PROBE_NP = 0'})}
for vn, v in VN.items():
    ranks = []
    for seed in range(1, 31):
        s = load_hub()
        s['ME'] = v
        pts = tournament_np(s, PG[0], PG[1], seed=seed, modes=['standard', 'discounted', 'stochastic', 'random'])
        o = sorted(pts, key=lambda n: -pts[n])
        ranks.append(o.index('ME') + 1)
    print(f'{vn:9s} top3 {sum(r <= 3 for r in ranks)}/30  mean rank {statistics.mean(ranks):.1f} of {len(s)}', flush=True)
