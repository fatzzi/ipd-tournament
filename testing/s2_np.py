# Sprint 2 N-Player: Public Goods b=0.3, c=1, groups of 5, weights points 50 / coop 30 / win 20.
# Scored like n_player_simulation.group_tournament + ranking.weighted_score. Field = textbook
# public-goods families drawn at random (no classmate code), many shuffles.
import sys, os, random, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2_1v1 import load
B, C, G = 0.3, 1, 5
W = {'points': 0.5, 'cooperation': 0.3, 'win_rate': 0.2}
MODES = ['standard', 'discounted', 'stochastic', 'random']

def th(t, end=0, start='C'):
    def f(l, m, o, meta):
        if end and meta['tournament_info'].get('mode') in ('standard', 'discounted') and meta['round'] >= 200 - end: return 'D'
        if not l: return start
        return 'C' if l.count('C') / len(l) >= t else 'D'
    return f
def alld(l, m, o, meta): return 'D'
def allc(l, m, o, meta): return 'C'
def rnd(p):
    def f(l, m, o, meta): return 'C' if meta['rng'].random() < p else 'D'
    return f
def grim(l, m, o, meta): return 'D' if any('D' in h for h in o) else 'C'
def freeride_end(k):
    def f(l, m, o, meta):
        if meta['round'] >= 200 - k: return 'D'
        if not l: return 'C'
        return 'C' if l.count('C') * 2 >= len(l) else 'D'
    return f
def lead_keeper(l, m, o, meta):  # defects whenever not strictly ahead of every rival
    if not o: return 'D'
    lead = min(h.count('C') for h in o) - m.count('C')
    return 'C' if lead >= 2 else 'D'

FAM = {
    'Maj': (8, lambda rg: th(0.5, rg.choice([0, 0, 1, 2]))), 'All': (4, lambda rg: th(1.0, rg.choice([0, 1]))),
    'Th75': (4, lambda rg: th(0.75, rg.choice([0, 1, 3]))), 'AllD': (4, lambda rg: alld), 'AllC': (2, lambda rg: allc),
    'Rand': (1, lambda rg: rnd(0.5)), 'Grim': (2, lambda rg: grim), 'FreeEnd': (3, lambda rg: freeride_end(rg.choice([1, 2, 5]))),
    'Lead': (2, lambda rg: lead_keeper),
}

def game_n(fs, mode, R, seed):
    n = len(fs); rng = random.Random(seed); H = [[] for _ in fs]; tot = [0.0] * n; played = 0
    lim = R if mode == 'random' else (2000 if mode == 'stochastic' else 200)
    ti = {'format': 'n_player', 'mode': mode, 'modes': MODES, 'n_players': n, 'rounds': 200, 'weights': W,
          'payoff_model': {'type': 'PublicGoodsPayoff', 'name': 'public_goods', 'b': B, 'c': C, 'nonlinear': {'type': 'linear'}}}
    for r in range(lim):
        if mode == 'stochastic' and r > 0 and rng.random() > 0.995: break
        mv = []
        for p in range(n):
            opp = [i for i in range(n) if i != p]
            mv.append(fs[p]([H[i][-1] for i in opp] if r else [], H[p][:], [H[i][:] for i in opp],
                            {'round': r, 'n_players': n, 'player_index': p, 'tournament_info': dict(ti), 'rng': rng}))
        k = mv.count('C'); w = 0.95 ** r if mode == 'discounted' else 1
        for p in range(n): tot[p] += (B * k - C * (mv[p] == 'C')) * w; H[p].append(mv[p])
        played += 1
    return tot, [h.count('C') for h in H], played

def tournament(strats, seed):
    names = sorted(strats); rng = random.Random(seed); idx = list(range(len(names))); rng.shuffle(idx)
    groups = [idx[i:i + G] for i in range(0, len(idx), G)]
    if len(groups) > 1 and len(groups[-1]) == 1: groups[-2].extend(groups.pop())
    R = random.Random(seed).randint(100, 300); cap = B * len(names) / len(groups) - C; out = {}
    for gi, g in enumerate(groups):
        fs = [strats[names[i]] for i in g]
        pts = [0.0] * len(g); ppr = [0.0] * len(g); cr = [0.0] * len(g)
        for mi, mode in enumerate(MODES):
            t, cc, pl = game_n(fs, mode, R, seed + gi * 10000 + mi)
            for j in range(len(g)): pts[j] += t[j]; ppr[j] += t[j] / pl; cr[j] += cc[j] / pl
        top = max(pts); winners = [j for j in range(len(g)) if abs(pts[j] - top) <= 1e-12]
        for j, i in enumerate(g):
            win = 1.0 if winners == [j] else 0.0
            p = max(0, min(1, ppr[j] / 4 / cap)); co = cr[j] / 4
            out[names[i]] = (W['win_rate'] * win + W['cooperation'] * co + W['points'] * p) * 100, win, co, p
    return out

def field(seed, size=64):
    rg = random.Random(seed); fams = list(FAM); out = {}
    for i in range(size):
        f = rg.choices(fams, [FAM[x][0] for x in fams])[0]
        out[f'{f}_{i}'] = FAM[f][1](rg)
    return out

if __name__ == '__main__':
    variants = {'now': {},

    }
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    st = {v: [] for v in list(variants) + ['before fix']}
    for sd in range(n):
        base = field(sd)
        me = {v: load('strategies/strategy.py', **s) for v, s in variants.items()}
        me['before fix'] = load(r'C:/Users/fxtim/AppData/Local/Temp/claude/C--Users-fxtim-Desktop-ipd-tournament/2a81a4e1-07e1-4ed4-be12-0eeb398ea05f/scratchpad/strategy_before.py')
        for v in me:
            f = dict(base); f['ME'] = me[v]
            # The ME slot replaces a random field member so the group layout varies.
            res = tournament(f, 1000 + sd)
            order = sorted(res, key=lambda x: -res[x][0])
            st[v].append((order.index('ME') + 1, *res['ME']))
    print(f"{'variant':12} mean_rank top3  score   win   coop  pts")
    for v, s in st.items():
        k = len(s)
        print(f'{v:12} {sum(x[0] for x in s)/k:8.1f} {sum(x[0]<=3 for x in s):3}/{k} {sum(x[1] for x in s)/k:6.1f} '
              f'{sum(x[2] for x in s)/k:5.2f} {sum(x[3] for x in s)/k:5.2f} {sum(x[4] for x in s)/k:5.2f}')
