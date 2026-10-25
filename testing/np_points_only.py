# N-Player under points-only ranking (Sprint 1 style: total points, highest first).
# Is always-defect the right fallback, or does cooperating with reciprocators and defecting
# only at the end score more? Field = textbook public-goods families (testing/s2_np.py).
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s2_np
from s2_np import field, game_n, MODES
from s2_1v1 import load

def ranks(strats, seed):
    names = sorted(strats); rng = random.Random(seed); idx = list(range(len(names))); rng.shuffle(idx)
    groups = [idx[i:i + 5] for i in range(0, len(idx), 5)]
    if len(groups) > 1 and len(groups[-1]) == 1: groups[-2].extend(groups.pop())
    R = random.Random(seed).randint(100, 300); pts = {}
    for gi, g in enumerate(groups):
        acc = [0.0] * len(g)
        for mi, mode in enumerate(MODES):
            t, _, _ = game_n([strats[names[i]] for i in g], mode, R, seed + gi * 10000 + mi)
            acc = [a + x for a, x in zip(acc, t)]
        for j, i in enumerate(g): pts[names[i]] = acc[j] / 4
    order = sorted(pts, key=lambda x: -pts[x])
    return order.index('ME') + 1, pts['ME']

if __name__ == '__main__':
    s2_np.W = {'points': 1.0, 'cooperation': 0.0, 'win_rate': 0.0}
    variants = {'always-D (now)': {}, 'coop+end10': {'POINTS_ONLY_NP': '1.1'},
                'coop+end30': {'POINTS_ONLY_NP': '1.1', 'ENDGAME_NP': '30'},
                'coop+end60': {'POINTS_ONLY_NP': '1.1', 'ENDGAME_NP': '60'}}
    for b in (0.4, 0.3):
        s2_np.B = b
        st = {v: [] for v in variants}
        for sd in range(int(sys.argv[1]) if len(sys.argv) > 1 else 30):
            base = field(sd)
            for v, subs in variants.items():
                f = dict(base); f['ME'] = load('strategies/strategy.py', **subs)
                st[v].append(ranks(f, 2000 + sd))
        print(f'b={b}  (64 players, points-only)')
        for v, s in st.items():
            k = len(s)
            print(f'  {v:16} mean_rank {sum(x[0] for x in s)/k:5.1f}  top3 {sum(x[0]<=3 for x in s):2}/{k}  '
                  f'zero-ish {sum(x[1] < 1 for x in s):2}/{k}  mean_pts {sum(x[1] for x in s)/k:6.1f}')
