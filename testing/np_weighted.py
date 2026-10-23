# N-Player with the REAL engine and the site's weighted ranking (default 33/34/33).
import sys, os, json, statistics, collections, ast
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
from hubfield import load_hub
from n_player_simulation import group_tournament
from payoff_models import PublicGoodsPayoff
BOTS = {'multiplicative_update', "Claude's_strategy", 'multiplicative_update_merciful', 'probabilistic_expectation', 'Salman', "Hijab's strategy"}
W = {'win_rate': 0.33, 'cooperation': 0.34, 'points': 0.33}
def score(e):
    g = e['wins'] + e['draws'] + e['losses']
    return (e['wins'] / g if g else 0) * W['win_rate'] + min(1, e['norm_cooperation_percentage'] / 100) * W['cooperation'] + e['points_percentage'] / 100 * W['points']
src = open(r'C:\Users\fxtim\Desktop\ipd-tournament\strategies\submit.py').read()
g = {}; exec(src, g); OURS = g['sentinel']

def last_k(k):
    # cooperate always; defect the last k rounds of 200-round modes
    def f(l, m, o, meta):
        r = meta.get('round', len(m))
        mode = (meta.get('tournament_info') or {}).get('mode')
        return 'D' if 200 - k <= r < 200 and mode in ('standard', 'discounted') else 'C'
    return f
def last_k_cond(k):
    # majority-conditional cooperator that defects in the last k rounds of any match it can see the length of
    def f(l, m, o, meta):
        r = meta.get('round', len(m))
        if 200 - k <= r < 200: return 'D'
        if not l: return 'C'
        return 'C' if l.count('C') * 2 >= len(l) else 'D'
    return f
def lead_coop(M, disc_safe=True):
    # Defect until we lead every rival by M (in units of c), then cooperate.
    # Relative payoff vs rival j per round = c*([j cooperated] - [we cooperated]); B(k) cancels.
    def f(l, m, o, meta):
        info = meta.get('tournament_info') or {}
        mode = info.get('mode')
        r = len(m)
        if r == 0:
            return 'D'
        disc = mode == 'discounted'
        w = [0.95 ** t if disc else 1.0 for t in range(r)]
        mine = sum(wt for wt, x in zip(w, m) if x == 'C')
        lead = min(sum(wt for wt, x in zip(w, h) if x == 'C') - mine for h in o) if o else 0
        need = M
        if disc and disc_safe:
            need = min(M, 20 * 0.95 ** r + 0.5)
        return 'C' if lead >= need else 'D'
    return f
def lead_giveup(M, K):
    # lead_coop, plus: if some rival has defected as much as we have over >= K rounds and is
    # still defecting, the group win is out of reach (best is a draw) -> cooperate fully.
    def f(l, m, o, meta):
        info = meta.get('tournament_info') or {}
        disc = info.get('mode') == 'discounted'
        r = len(m)
        if r == 0:
            return 'D'
        mineC = m.count('C')
        if r >= K:
            for h in o:
                if h.count('C') <= mineC and 'C' not in h[-K:]:
                    return 'C'
        w = [0.95 ** t if disc else 1.0 for t in range(r)]
        mine = sum(wt for wt, x in zip(w, m) if x == 'C')
        lead = min(sum(wt for wt, x in zip(w, h) if x == 'C') - mine for h in o) if o else 0
        need = min(M, 20 * 0.95 ** r + 0.5) if disc else M
        return 'C' if lead >= need else 'D'
    return f
CANDS = {'ours_now': OURS, 'alwaysD': lambda l, m, o, meta: 'D', 'alwaysC': lambda l, m, o, meta: 'C',
         'lastD1': last_k(1), 'lastD3': last_k(3), 'lastD10': last_k(10), 'condLast3': last_k_cond(3), 'lead2': lead_coop(2), 'lead4': lead_coop(4), 'lead8': lead_coop(8), 'lead4_nodisc': lead_coop(4, False), 'give5': lead_giveup(4, 5), 'give10': lead_giveup(4, 10), 'give3': lead_giveup(4, 3)}
want = sys.argv[1:] or list(CANDS)
N = 30
for cn in want:
    ranks = []; parts = []
    for seed in range(1, N + 1):
        hub = load_hub(); hub.pop('yay', None); hub['ME'] = CANDS[cn]
        strats = [{'name': n, 'code': '', 'func': f} for n, f in hub.items()]
        res = group_tournament(strats, rounds=200, group_size=5, seed=seed,
                               payoff_model=PublicGoodsPayoff(b=0.4, c=1.0), weights=W,
                               modes=['standard', 'discounted', 'stochastic', 'random'])
        lb = res['leaderboard']
        sc = {e['name']: score(e) for e in lb}
        o = [n for n in sorted(sc, key=lambda n: -sc[n]) if n not in BOTS]
        ranks.append(o.index('ME') + 1)
        me = next(e for e in lb if e['name'] == 'ME')
        parts.append((me['wins'], round(me['norm_cooperation_percentage']), round(me['points_percentage'], 1)))
    print(f'{cn:10s} student-rank top3 {sum(r <= 3 for r in ranks)}/{N}  mean {statistics.mean(ranks):.1f}  wins {sum(p[0] for p in parts)}/{N}  coop% {statistics.mean(p[1] for p in parts):.0f}  pts% {statistics.mean(p[2] for p in parts):.1f}', flush=True)
