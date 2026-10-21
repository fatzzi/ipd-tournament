import sys, statistics
from field import FIELD, np_threshold, careful, guide_adapts, np_freerider_end, alld
from sim import tournament_np
src=open(sys.argv[1]).read()
def load(**rep):
    s=src
    for a,b in rep.items(): s=s.replace(a,b)
    g={}; exec(s,g); return g['sentinel']
V={'cur':{},
   'slack1':{'FREE_RIDE_SLACK = 0':'FREE_RIDE_SLACK = 1'},
   'doomed':{'DOOMED_D = False':'DOOMED_D = True'},
   'slack1+doomed':{'FREE_RIDE_SLACK = 0':'FREE_RIDE_SLACK = 1','DOOMED_D = False':'DOOMED_D = True'},
   'slack1+doomed+noOlive':{'FREE_RIDE_SLACK = 0':'FREE_RIDE_SLACK = 1','DOOMED_D = False':'DOOMED_D = True','OLIVE = True':'OLIVE = False'},
   'slack1+doomed+share75':{'FREE_RIDE_SLACK = 0':'FREE_RIDE_SLACK = 1','DOOMED_D = False':'DOOMED_D = True','COOP_SHARE = 0.5':'COOP_SHARE = 0.75'},
}
variants={k:load(**v) for k,v in V.items()}; variants['AllD']=alld
def fields():
    yield 'base', dict(FIELD)
    f=dict(FIELD)
    for i in range(4): f[f'Guide{i}']=guide_adapts; f[f'Careful{i}']=careful; f[f'Th75_{i}']=np_threshold(0.75); f[f'FreeEnd{i}']=np_freerider_end
    yield 'crowd', f
tot={k:0 for k in variants}
for fname,f in fields():
    for (b,gs) in ((0.4,5),(0.3,5),(0.25,8)):
        line=[]
        for vn,v in variants.items():
            ranks=[]
            for seed in range(1,31):
                s=dict(f); s['ME']=v
                pts=tournament_np(s,b,gs,seed=seed,modes=['standard','stochastic','random'])
                order=sorted(pts,key=lambda n:-pts[n]); ranks.append(order.index('ME')+1)
            t3=sum(r<=3 for r in ranks); tot[vn]+=t3
            line.append(f"{vn}:{t3}")
        print(fname,b,gs,' '.join(line),flush=True)
print('TOTAL top3 hits /180:',tot)
