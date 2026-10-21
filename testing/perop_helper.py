import random
from sim import game, MATS, MODES
def total_vs(me, field, mk='S1', seeds=(1, 2, 3)):
    ti = {'weights': {'points': 1}, 'payoff_matrix': MATS[mk], 'format': '2-player'}
    tot = 0
    for on, of in field.items():
        for seed in seeds:
            R = random.Random(seed).randint(100, 300)
            for mi, mode in enumerate(MODES):
                tot += game(me, of, MATS[mk], mode, R, seed * 1000 + mi, ti)[0] / (4 * len(seeds))
    return tot
