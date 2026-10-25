# Sprint 2 OS tuning: Priority scheduler, 8 cores, 100 tasks, 10 runs, homogeneous.
# Simple busy-signal rules only, compared on several seed bases (no classmate code).
import sys, json
sys.path.insert(0, r'C:/Users/fxtim/AppData/Local/Temp/v140/COMPUTATION-NOT-FOUND-ipd-app-cb47fd6')
from core_simulation import run_full_simulation

def rule(K, m=1, calm='D'):
    other = 'C' if calm == 'D' else 'D'
    return f'''
def s(last_moves, my_history, opponents_histories, meta):
    if not last_moves or last_moves[0] == 'D':
        return 'C'
    past = opponents_histories[0][-{K}:] if {K} else []
    return 'C' if past.count('D') >= {m} else '{calm}'
'''
cands = {'allC': "def s(a,b,c,d):\n    return 'C'\n", 'allD': "def s(a,b,c,d):\n    return 'D'\n",
         'guideInv': "def s(a,b,c,d):\n    return 'D' if a and a[0]=='D' else 'C'\n"}
for K in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12):
    cands[f'K{K}'] = rule(K)
for K, m in ((5, 2), (6, 2), (7, 2), (8, 2), (7, 3), (9, 3), (10, 3), (12, 4)):
    cands[f'K{K}m{m}'] = rule(K, m)
if __name__ == '__main__':
    seeds = [int(x) for x in sys.argv[1:]] or [29257, 1, 1000, 424242]
    res = {}
    for sd in seeds:
        r = run_full_simulation([{'name': n, 'code': c} for n, c in cands.items()], num_cores=8, seed=sd,
                                scheduler='priority', runs=10, num_processes=100)
        res[sd] = {n: (v['avg']['avg_response'], v['avg']['avg_waiting']) for n, v in r['strategies'].items()}
        res[sd]['_baseline'] = (r['baseline']['avg']['avg_response'], r['baseline']['avg']['avg_waiting'])
        print(sd, r['errors'], flush=True)
    names = list(cands) + ['_baseline']
    print(f"{'rule':10}" + ''.join(f'{sd:>16}' for sd in seeds) + '   mean')
    for n in sorted(names, key=lambda n: sum(res[s][n][0] for s in seeds)):
        print(f'{n:10}' + ''.join(f'{res[s][n][0]:>9.2f}/{res[s][n][1]:<6.1f}' for s in seeds)
              + f'   {sum(res[s][n][0] for s in seeds)/len(seeds):.3f}')
