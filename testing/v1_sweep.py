import sys, statistics
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
from hubfield import load_hub
from sim import tournament_1v1, MATS
src = open(r'C:\Users\fxtim\Desktop\ipd-tournament\strategies\strategy.py').read()
rep = dict(a.split('=>') for a in sys.argv[2:])
for a, b in rep.items():
    assert a in src, a; src = src.replace(a, b)
g = {}; exec(src, g); ME = g['sentinel']
BOTS = {'multiplicative_update', "Claude's_strategy", 'multiplicative_update_merciful', 'probabilistic_expectation', 'Salman', "Hijab's strategy"}
pr, er, o2 = [], [], []
for seed in range(1, 9):
    s = load_hub(); s.pop('yay', None); s['ME'] = ME
    for w, lst in (({'points': 1}, pr), ({'win_rate': 1, 'cooperation': 1, 'points': 1}, er)):
        out = tournament_1v1(s, MATS['S1'], seed=seed, weights=w)
        o = [n for n in sorted(out, key=lambda n: -out[n]['weighted']) if n not in BOTS]
        lst.append(o.index('ME') + 1)
        if w == {'points': 1}: o2.append(out['ME']['ptspct'])
print(sys.argv[1], 'pts-only mean', round(sum(o2)/len(o2),4), 'points-only student ranks', pr, 'top3', sum(r<=3 for r in pr), '| equal', er, 'top3', sum(r<=3 for r in er), flush=True)
