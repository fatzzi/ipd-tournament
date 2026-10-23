# N-Player, REAL engine, Sprint 1 POINTS-ONLY ranking:
#   sort by points_percentage desc, then cooperation% desc, then win rate desc (the FAQ tiebreak).
# Confirms whether pure free-riding (always D) is still best, or whether the coop% tiebreak
# among clustered defectors rewards a touch of cooperation.
import sys, statistics
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
from hubfield import load_hub
from n_player_simulation import group_tournament
from payoff_models import PublicGoodsPayoff

BOTS = {'multiplicative_update', "Claude's_strategy", 'multiplicative_update_merciful',
        'probabilistic_expectation', 'Salman', "Hijab's strategy"}
src = open(r'C:\Users\fxtim\Desktop\ipd-tournament\strategies\strategy.py', encoding='utf-8').read()
g = {}; exec(src, g); OURS = g['sentinel']

def key(e):
    tg = e['wins'] + e['draws'] + e['losses']
    return (e['points_percentage'], e['norm_cooperation_percentage'], e['wins'] / tg if tg else 0)

def coop_eps(eps):
    # Always defect, except cooperate on the first `eps` rounds -> tiny coop% to win ties.
    def f(l, m, o, meta):
        return 'C' if len(m) < eps else 'D'
    return f

CANDS = {'ours': OURS, 'alwaysD': lambda l, m, o, meta: 'D',
         'D+coop2': coop_eps(2), 'D+coop5': coop_eps(5), 'D+coop10': coop_eps(10)}
N = 30
print('== N-Player Sprint 1 points-only (b=0.4, groups of 5, 30 shuffles)')
for cn, fn in CANDS.items():
    ranks = []; pp = []; cp = []
    for seed in range(1, N + 1):
        hub = load_hub(); hub.pop('yay', None); hub['ME'] = fn
        strats = [{'name': n, 'code': '', 'func': f} for n, f in hub.items()]
        res = group_tournament(strats, rounds=200, group_size=5, seed=seed,
                               payoff_model=PublicGoodsPayoff(b=0.4, c=1.0),
                               weights={'points': 1.0}, modes=['standard', 'discounted', 'stochastic', 'random'])
        lb = res['leaderboard']
        order = [e['name'] for e in sorted(lb, key=key, reverse=True) if e['name'] not in BOTS]
        ranks.append(order.index('ME') + 1)
        me = next(e for e in lb if e['name'] == 'ME')
        pp.append(me['points_percentage']); cp.append(me['norm_cooperation_percentage'])
    print(f'{cn:9s} top3 {sum(r <= 3 for r in ranks)}/{N}  mean rank {statistics.mean(ranks):.1f}  '
          f'pts% {statistics.mean(pp):.2f}  coop% {statistics.mean(cp):.1f}', flush=True)
