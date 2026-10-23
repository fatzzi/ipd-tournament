from common import *
from hubfield import load_hub
from n_player_simulation import group_tournament
from payoff_models import PublicGoodsPayoff
W = {'win_rate': 0.33, 'cooperation': 0.34, 'points': 0.33}
def score(e):
    g = e['wins'] + e['draws'] + e['losses']
    return (e['wins'] / g if g else 0) * .33 + min(1, e['norm_cooperation_percentage'] / 100) * .34 + e['points_percentage'] / 100 * .33
hub = load_hub(GAL)
for seed in (1, 2, 3):
    strats = [{'name': n, 'code': '', 'func': f} for n, f in hub.items()]
    res = group_tournament(strats, rounds=200, group_size=5, seed=seed, payoff_model=PublicGoodsPayoff(b=0.4, c=1.0), weights=W, modes=['standard', 'discounted', 'stochastic', 'random'])
    lb = sorted(res['leaderboard'], key=lambda e: -score(e))
    print(f'\n== N-Player seed {seed} (b=0.4, groups of 5, equal weights)')
    k = 0
    for i, e in enumerate(lb, 1):
        n = e['name']
        if n not in BOTS: k += 1
        if i <= 12 or n == 'yay':
            print(f'{i:2d} ({"s"+str(k) if n not in BOTS else "--"}) {score(e)*100:6.2f}  win {e["wins"]} draw {e["draws"]} coop {e["norm_cooperation_percentage"]:5.1f} pts {e["points_percentage"]:5.1f}  {tag(n)}', flush=True)
