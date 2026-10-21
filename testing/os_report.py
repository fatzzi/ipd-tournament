# Summarise local-only/os_study results for one setting against the guide's rule.
import sys, json, statistics, glob, os
pre = sys.argv[1]  # e.g. round_robin_8_100
R = {os.path.basename(f)[len(pre) + 1:-5]: json.load(open(f))
     for f in glob.glob(os.path.join(os.path.dirname(__file__), '..', 'local-only', 'os_study', pre + '_*.json'))}
g = R['guide']; n = len(g)
print(f'{"candidate":10s} {"mean":>8s}  beats guide in 10-seed windows   per-seed wins')
for c in sorted(R, key=lambda c: statistics.mean(R[c])):
    w = [statistics.mean(R[c][i:i + 10]) < statistics.mean(g[i:i + 10]) for i in range(n - 9)]
    print(f'{c:10s} {statistics.mean(R[c]):8.3f}   {sum(w):3d}/{len(w)}   {sum(a < b for a, b in zip(R[c], g))}/{n}')
