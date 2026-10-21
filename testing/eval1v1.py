import sys, statistics, importlib.util
from field import FIELD
from sim import tournament_1v1, MATS
spec=importlib.util.spec_from_file_location('s', sys.argv[1]); s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
me=s.sentinel
WEIGHTS={'points':{'points':1},'balanced':{'win_rate':1/3,'cooperation':1/3,'points':1/3},'wins':{'win_rate':1}}
for mk in ('S1','F'):
    for wk,w in WEIGHTS.items():
        ranks=[];metric='weighted'
        for seed in range(1,4):
            strats=dict(FIELD); strats['ME']=me
            out=tournament_1v1(strats,MATS[mk],seed=seed,weights=w)
            order=sorted(out,key=lambda n:-out[n][metric]); ranks.append(order.index('ME')+1)
        top=order[:5]
        print(f"{mk} {wk:9s} ME ranks {ranks} of {len(strats)} | last top5: "+", ".join(f"{n}({out[n][metric]:.3f})" for n in top), f"| ME {out['ME'][metric]:.3f} win {out['ME']['win']:.2f} coop {out['ME']['coop']:.2f}")
