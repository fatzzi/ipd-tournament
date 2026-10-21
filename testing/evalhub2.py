import sys
from hubfield import load_hub
from field import FIELD
from sim import tournament_1v1, MATS
src=open(sys.argv[1]).read()
def ld(**rep):
    s=src
    for a,b in rep.items(): s=s.replace(a,b)
    g={}; exec(s,g); return g['sentinel']
V={'new':ld(),'no_peek':ld(**{'last_round = probe.random() > STOCHASTIC_CONTINUE':'last_round = False'}),
   'no_trail':ld(**{'WIN_SHARE = 0.25':'WIN_SHARE = 2'}),'old':ld(**{'last_round = probe.random() > STOCHASTIC_CONTINUE':'last_round = False','WIN_SHARE = 0.25':'WIN_SHARE = 2'})}
for fname in ('hub','hub+synthetic'):
  for wk,w in (('points',{'points':1}),('equal',{'win_rate':1,'cooperation':1,'points':1})):
    line=[]
    for vn,v in V.items():
        ranks=[]
        for seed in (1,2,3):
            s=load_hub(sys.argv[2])
            if fname!='hub': s.update(FIELD)
            s['ME']=v
            out=tournament_1v1(s,MATS['S1'],seed=seed,weights=w)
            o=sorted(out,key=lambda n:-out[n]['weighted']); ranks.append(o.index('ME')+1)
        line.append(f"{vn} {ranks} win {out['ME']['win']:.2f}")
    print(fname,wk,len(s),' | '.join(line),flush=True)
