from common import *
from hubfield import load_hub
from sim import tournament_1v1, MATS
s = load_hub(GAL)
for wk, w in (('EQUAL weights 33/34/33', {'win_rate': .33, 'cooperation': .34, 'points': .33}), ('POINTS only', {'points': 1})):
    out = tournament_1v1(s, MATS['S1'], seed=1, weights=w)
    o = sorted(out, key=lambda n: -out[n]['weighted'])
    print(f'\n== 1v1 {wk} (seed 1, {len(o)} entries)')
    k = 0
    for i, n in enumerate(o, 1):
        if n not in BOTS: k += 1
        e = out[n]
        print(f'{i:2d} ({"s"+str(k) if n not in BOTS else "--"}) {e["weighted"]*100:6.2f}  win {e["win"]:.2f} coop {e["coop"]:.2f} pts {e["ptspct"]:.3f}  {tag(n)}', flush=True)
