# Average 1v1 score per opponent (all four modes, several seeds) for ME and the leaders.
import sys, random
from hubfield import load_hub
from sim import game, MATS, MODES
g = {}; exec(open(sys.argv[1]).read(), g)
field = load_hub()
players = {'ME': g['sentinel'], **{k: field[k] for k in sys.argv[2:]}}
ti = {'weights': {'points': 1}, 'payoff_matrix': MATS['S1'], 'format': '2-player'}
print(f"{'opponent':30s}" + ''.join(f'{p[:12]:>13s}' for p in players))
tot = {p: 0 for p in players}
for on, of in field.items():
    row = []
    for pn, pf in players.items():
        if pn == on: row.append(float('nan')); continue
        s = 0
        for seed in range(1, 4):
            R = random.Random(seed).randint(100, 300)
            for mi, mode in enumerate(MODES):
                s += game(pf, of, MATS['S1'], mode, R, seed * 1000 + mi, ti)[0]
        row.append(s / 12); tot[pn] += s / 12 if pn != on else 0
    print(f'{on:30s}' + ''.join(f'{x:13.3f}' for x in row))
print('TOTAL'.ljust(30) + ''.join(f'{tot[p]:13.2f}' for p in players))
