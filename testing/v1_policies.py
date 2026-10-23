# Search 1v1 POLICY space for Sprint 1 points-only ranking, against the hidden-code field.
# Candidate 1v1 policies defined directly (4-arg signature). Fast exact harness: opp-vs-opp
# cached per seed; each candidate only plays vs every opponent. Endgame here = defect at the
# very last fixed round (r==199); the winner is ported into strategy.py with full stochastic
# handling afterwards.
#   python testing/v1_policies.py [+base] [NSEED]
import sys, random, statistics
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
from hubfield import load_hub
from sim import game, MATS, MODES
import field as F

MAT = MATS['S1']; MX = max(v[0] for v in MAT.values())
TI = {'weights': {'points': 1}, 'payoff_matrix': MAT, 'format': '2-player', 'n_players': 2, 'payoff_model': 'standard'}
BOTS = {'multiplicative_update', "Claude's_strategy", 'multiplicative_update_merciful',
        'probabilistic_expectation', 'Salman', "Hijab's strategy"}
END = 199  # defect at r==END in fixed-length modes

def endgame(meta):
    return meta.get('round', 0) >= END

def tft(l, m, o, meta):
    if endgame(meta): return 'D'
    return o[0][-1] if o and o[0] else 'C'

def gtft(g):
    def f(l, m, o, meta):
        if endgame(meta): return 'D'
        h = o[0] if o else []
        if not h: return 'C'
        if h[-1] == 'C': return 'C'
        return 'C' if meta['rng'].random() < g else 'D'
    return f

def tf2t(l, m, o, meta):  # punish only two defections in a row -> forgiving
    if endgame(meta): return 'D'
    h = o[0] if o else []
    return 'D' if len(h) >= 2 and h[-1] == 'D' and h[-2] == 'D' else 'C'

def pavlov(l, m, o, meta):
    if endgame(meta): return 'D'
    h = o[0] if o else []
    if not h: return 'C'
    return m[-1] if h[-1] == 'C' else ('D' if m[-1] == 'C' else 'C')

def contrite(detector, gen=0.0):
    # Contrite TFT: forgive our own provoked defections; optional responsiveness detector;
    # optional generous forgiveness of their defection. (Mirrors strategy.py's 1v1 core.)
    def f(l, m, o, meta):
        if endgame(meta): return 'D'
        opp = o[0] if o else []
        n = len(opp)
        if not opp: return 'C'
        if detector and n >= 20:
            lo = max(0, n - 1 - 30)
            ac = [opp[t + 1] for t in range(lo, n - 1) if m[t] == 'C']
            ad = [opp[t + 1] for t in range(lo, n - 1) if m[t] == 'D']
            if len(ac) >= 5 and len(ad) >= 5:
                pc = ac.count('C') / len(ac); pd = ad.count('C') / len(ad)
                if (pc - pd < 0.2 and pc < 0.8) or pc < 0.6: return 'D'
        if opp[-1] == 'C': return 'C'
        if n >= 2 and m[-2] == 'D' and opp[-2] == 'C' and m[-1] == 'C': return 'C'
        if n >= 2 and m[-2] == 'D':
            j = n - 2
            while j > 0 and m[j - 1] == 'D': j -= 1
            if j >= 1 and opp[j - 1] == 'C' and opp[j] == 'C': return 'C'
        run = 0
        for t in range(n - 1, -1, -1):
            if opp[t] == 'D' and m[t] == 'D': run += 1
            else: break
        if run >= 3 and opp.count('C') * 2 > n and run % 4 == 3: return 'C'
        if gen and meta['rng'].random() < gen: return 'C'
        return 'D'
    return f

def cutoff(base, thr=0.45):
    # base policy, but once enough rounds are seen, defect fully against anyone whose
    # overall cooperation rate is below `thr` (Ismile / fatima use a 45% cutoff).
    def f(l, m, o, meta):
        if endgame(meta): return 'D'
        h = o[0] if o else []
        n = len(h)
        if n >= 10 and h.count('C') < thr * n: return 'D'
        return base(l, m, o, meta)
    return f

def gradual(l, m, o, meta):
    # Beaufils' Gradual: default C; on each opponent defection, defect (total opp defections)
    # times in a row, then play C,C to rebuild. Forgiving but escalating.
    if endgame(meta): return 'D'
    h = o[0] if o else []
    n = len(h)
    if n == 0: return 'C'
    pun = calm = 0
    for t in range(n):
        if pun > 0:
            pun -= 1
            if pun == 0: calm = 2
        elif calm > 0:
            calm -= 1
        if h[t] == 'D' and pun == 0 and calm == 0:
            pun = h[:t + 1].count('D')
    if pun > 0: return 'D'
    return 'C'

def exploit_pushover(l, m, o, meta):
    # Contrite TFT, but if the opponent has cooperated on every one of the last 15 rounds
    # while we defected at least 3 times in that window (they never punish) -> exploit (all D).
    if endgame(meta): return 'D'
    opp = o[0] if o else []
    n = len(opp)
    if not opp: return 'C'
    if n >= 15:
        w_opp = opp[-15:]; w_me = m[-15:]
        if w_opp.count('D') == 0 and w_me.count('D') >= 3:
            return 'D'
    if opp[-1] == 'C': return 'C'
    if n >= 2 and m[-2] == 'D' and opp[-2] == 'C' and m[-1] == 'C': return 'C'
    return 'D'

CANDS = {
    'TFT'            : tft,
    'GTFT.10'        : gtft(0.10),
    'GTFT.20'        : gtft(0.20),
    'TF2T'           : tf2t,
    'Pavlov'         : pavlov,
    'contrite+det'   : contrite(True),
    'contrite-det'   : contrite(False),
    'contrite+gen.1' : contrite(True, 0.10),
    'contrite-det+gen.1': contrite(False, 0.10),
    'contrite-det+gen.2': contrite(False, 0.20),
    'exploit_push'   : exploit_pushover,
    'gradual'        : gradual,
    'TFT_cut'        : cutoff(tft),
    'GTFT.1_cut'     : cutoff(gtft(0.10)),
    'contrite-det+gen.1_cut': cutoff(contrite(False, 0.10)),
    'contrite+det_cut': cutoff(contrite(True)),
}

addbase = '+base' in sys.argv
nums = [a for a in sys.argv[1:] if a.isdigit()]
NSEED = int(nums[0]) if nums else 6
agg = {c: {'pp': [], 'rank': []} for c in CANDS}

def play(fa, fb, seed):
    ra = rb = mv = 0
    for mi, mode in enumerate(MODES):
        _, _, pa, pb, _, _, r = game(fa, fb, MAT, mode, R, seed + mi, TI)
        ra += pa; rb += pb; mv += r
    return ra, rb, mv

for seed in range(1, NSEED + 1):
    hub = load_hub(); hub.pop('yay', None)
    if addbase:
        for bn, bf in F.FIELD.items(): hub.setdefault('B_' + bn, bf)
    names = sorted(hub); funcs = [hub[n] for n in names]
    R = random.Random(seed).randint(100, 300)
    braw = {n: 0 for n in names}; bmv = {n: 0 for n in names}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ra, rb, mv = play(funcs[i], funcs[j], seed + (i * 1000 + j) * 7 + 500000)
            braw[names[i]] += ra; bmv[names[i]] += mv; braw[names[j]] += rb; bmv[names[j]] += mv
    for cn, me in CANDS.items():
        raw = dict(braw); mv = dict(bmv); mr = mm = 0
        for k, n in enumerate(names):
            a, b, m = play(me, funcs[k], seed + k * 1000)
            mr += a; mm += m; raw[n] += b; mv[n] += m
        pp = {n: raw[n] / mv[n] / MX for n in names}; pp['ME'] = mr / mm / MX
        order = [n for n in sorted(pp, key=lambda n: -pp[n]) if n not in BOTS]
        agg[cn]['pp'].append(pp['ME']); agg[cn]['rank'].append(order.index('ME') + 1)

print(f'== 1v1 POINTS-ONLY policy search ({NSEED} seeds, field: {"snapshot+baselines" if addbase else "snapshot only"})')
print(f'{"policy":20s}  {"mean pts%":>9s}  {"top3":>6s}  {"meanRank":>8s}  ranks')
for cn in sorted(CANDS, key=lambda c: -statistics.mean(agg[c]['pp'])):
    r = agg[cn]['rank']
    print(f'{cn:20s}  {statistics.mean(agg[cn]["pp"])*100:9.3f}  {sum(x<=3 for x in r):>3d}/{len(r):<2d}  '
          f'{statistics.mean(r):8.2f}  {r}', flush=True)
