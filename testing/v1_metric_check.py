# v1.4.0 ranks 1v1 by TOTAL_POINTS (sum over opponents of the mode-averaged per-round score),
# tiebreak cooperation% then win rate -- NOT by points_percentage, which my earlier sweeps used.
# This checks whether our rank differs under the real metric. sim.py's out[n]['points'] == the
# engine's total_points; out[n]['ptspct'] == points_percentage.
import sys, statistics
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
from hubfield import load_hub
from sim import tournament_1v1, MATS
g = {}; exec(open(r'C:\Users\fxtim\Desktop\ipd-tournament\strategies\strategy.py', encoding='utf-8').read(), g)
OURS = g['sentinel']
BOTS = {'multiplicative_update', "Claude's_strategy", 'multiplicative_update_merciful',
        'probabilistic_expectation', 'Salman', "Hijab's strategy"}

def rank_by(out, keyfn):
    order = [n for n in sorted(out, key=keyfn) if n not in BOTS]
    return order.index('ME') + 1

tp_ranks, pp_ranks = [], []
for seed in range(1, 9):
    s = load_hub(); s.pop('yay', None); s['ME'] = OURS
    out = tournament_1v1(s, MATS['S1'], seed=seed, weights={'points': 1})
    # Real metric: total_points desc, tiebreak cooperation% desc, win rate desc
    tp_ranks.append(rank_by(out, lambda n: (-out[n]['points'], -out[n]['coop'], -out[n]['win'])))
    # Old metric I used: points_percentage desc
    pp_ranks.append(rank_by(out, lambda n: -out[n]['ptspct']))
print('field size', len(s))
print(f'rank by TOTAL_POINTS (real v1.4.0 metric): {tp_ranks}  top3 {sum(r<=3 for r in tp_ranks)}/8  mean {statistics.mean(tp_ranks):.2f}')
print(f'rank by points_percentage (old harness)  : {pp_ranks}  top3 {sum(r<=3 for r in pp_ranks)}/8  mean {statistics.mean(pp_ranks):.2f}')
