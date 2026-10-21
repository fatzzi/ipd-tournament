# How often does each OS candidate beat the guide's busy/calm rule, scored like the site
# (mean avg_response over 10 consecutive seeds, all four workloads)?
# usage: python testing/os_study.py <scheduler> <cores> <tasks> <first_seed> <n_seeds> <candidate>
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'local-only', 'ipd-app'))
from core_simulation import OSSimulator, WORKLOAD_PROFILES


def calm_p(p, first='C'):
    def f(l, m, o, meta):
        if not l:
            return first
        if l[0] == 'D':
            return 'C'
        return 'C' if meta['rng'].random() < p else 'D'
    return f


def ismile(l, m, o, meta):
    if not l:
        return 'C'
    h = o[0]
    if len(h) >= 4 and h[-4:] == ['C', 'C', 'C', 'C']:
        return 'C'
    return 'D'


def calm_every(k):
    # deterministic version of calm_p: yield on every k-th calm dispatch of this core
    def f(l, m, o, meta):
        if not l or l[0] == 'D':
            return 'C'
        return 'C' if len(m) % k == 0 else 'D'
    return f


def window(k):
    # yield if the system was busy at any of this core's last k dispatches
    def f(l, m, o, meta):
        if not l:
            return 'C'
        return 'C' if 'D' in o[0][-k:] else 'D'
    return f


def decoded(on_false_alarm):
    # Cores share one function object, so they can share memory. Track every core's last
    # move; when the "busy" signal fires only because most other cores are holding the CPU
    # (not because of a real queue), play `on_false_alarm` instead of yielding.
    def f(l, m, o, meta):
        me = meta['player_index']
        nc = meta['n_players']
        st = f.state
        if meta['round'] == 0:
            st[me] = 'C'
        if not l:
            st[me] = 'C'
            return 'C'
        if l[0] == 'D':
            holders = sum(1 for j in range(nc) if j != me and st.get(j) == 'D')
            move = on_false_alarm if holders * 2 >= nc - 1 else 'C'
        else:
            move = 'D'
        st[me] = move
        return move
    f.state = {}
    return f


CANDS = {'win2': window(2), 'win3': window(3), 'dec_D': decoded('D'),
         'guide': calm_p(0.0), 'p0.1': calm_p(0.1), 'p0.2': calm_p(0.2), 'p0.3': calm_p(0.3),
         'p0.4': calm_p(0.4), 'allC': calm_p(1.0), 'ismile': ismile,
         'every3': calm_every(3), 'every4': calm_every(4), 'every5': calm_every(5)}

sch, nc, nt, s0, ns, cand = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
f = CANDS[cand]
res = []
for s in range(s0, s0 + ns):
    v = 0
    for wl in WORKLOAD_PROFILES:
        sim = OSSimulator(wl, [f] * nc, scheduler=sch, seed=s, num_cores=nc)
        sim.generate_workload(nt)
        v += sim.run()['global_metrics']['avg_response'] / 4
    res.append(v)
out = os.path.join(HERE, '..', 'local-only', 'os_study')
os.makedirs(out, exist_ok=True)
json.dump(res, open(os.path.join(out, f'{sch}_{nc}_{nt}_{cand}.json'), 'w'))
print(cand, 'done')
