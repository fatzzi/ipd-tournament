import sys, statistics
sys.path.insert(0, sys.argv[1])
from core_simulation import run_full_simulation
mine=open(sys.argv[2]).read()
guide="def g(l,m,o,meta):\n    if not l:\n        return 'C'\n    return 'C' if l[0]=='D' else 'D'"
allc="def c(l,m,o,meta):\n    return 'C'"
sch,nc,nt=sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
for seed in (11,):
    r=run_full_simulation([{'name':'mine','code':mine},{'name':'guide','code':guide},{'name':'allC','code':allc}],num_cores=nc,seed=seed,scheduler=sch,runs=10,num_processes=nt)
    print(sch,nc,nt,[(k,v['avg'].get('avg_response'),v['avg'].get('ci',{}).get('avg_response')) for k,v in r['strategies'].items()], r['errors'],flush=True)
