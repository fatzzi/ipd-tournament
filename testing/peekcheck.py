import sys, random
from hubfield import ns
from core_simulation import extract_strategy_func
from sim import game, MATS
code=open(sys.argv[1]).read()
print('safe:', ns['is_safe_code'](code))
tft=lambda l,m,o,meta: l[0] if l else 'C'
hits=total=0
for seed in range(40):
    f=extract_strategy_func(code, seed=1)   # real sandbox builtins + guarded import
    log=[]
    def wrap(l,m,o,meta): mv=f(l,m,o,meta); log.append(mv); return mv
    r=game(wrap,tft,MATS['S1'],'stochastic',200,seed,{'weights':{'points':1},'payoff_matrix':MATS['S1'],'format':'2-player'})
    n=r[6]; total+=1
    last_d = log[-1]=='D'; mid_d=[i for i,x in enumerate(log[:-1]) if x=='D' and not (197<=i<200)]
    hits+=last_d
    if seed<6: print(f'seed {seed}: {n} rounds, last move {log[-1]}, other unexpected Ds at {mid_d[:6]}')
print(f'defected on the true last round in {hits}/{total} stochastic matches')
