import sys, statistics, time
sys.path.insert(0, sys.argv[1])
from core_simulation import OSSimulator, WORKLOAD_PROFILES
def make(p, first):
    def f(l,m,o,meta):
        if not l: return first
        if l[0]=='D': return 'C'
        return 'C' if meta['rng'].random() < p else 'D'
    return f
cands={f'p{p} first{fi}':make(p,fi) for p in (0.2,0.3,0.45,0.6,0.75) for fi in ('C',)}
cands['p0.3 firstD']=make(0.3,'D')
SET={'S1':('round_robin',8,100),'S2':('priority',8,200),'Final':('priority',4,200)}
label=sys.argv[4]; sch,nc,nt=SET[label]
seeds=list(range(int(sys.argv[2]), int(sys.argv[2])+int(sys.argv[3])))
res=[]
for name,f in cands.items():
    ov=[]
    for s in seeds:
        ov.append(sum(OSSimulator(wl,[f]*nc,scheduler=sch,seed=s,num_cores=nc).__class__ and 0 for wl in []) or 0)
        v=0
        for wl in WORKLOAD_PROFILES:
            sim=OSSimulator(wl,[f]*nc,scheduler=sch,seed=s,num_cores=nc); sim.generate_workload(nt)
            v+=sim.run()['global_metrics']['avg_response']/4
        ov[-1]=v
    res.append((statistics.mean(ov),statistics.stdev(ov),name))
print('==',label,' '.join(f'{n}={v:.2f}±{sd:.1f}' for v,sd,n in sorted(res)),flush=True)
