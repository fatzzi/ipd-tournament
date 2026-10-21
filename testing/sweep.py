import sys, importlib.util, statistics
from field import FIELD, endgame_tft, claude_gtft_endgame
from sim import tournament_1v1, MATS
src=open(sys.argv[1]).read()
def load(depth):
    g={}; exec(src.replace('ENDGAME_1V1 = 3','ENDGAME_1V1 = %d'%depth),g); return g['sentinel']
def tough():
    f=dict(FIELD)
    for i in range(3): f[f'E2_{i}']=endgame_tft(2); f[f'E3_{i}']=endgame_tft(3); f[f'GT{i}']=claude_gtft_endgame
    for d in (1,2,3,4): f[f'Twin{d}']=load(d)   # other people with my idea
    return f
for fname,mk in (('base',FIELD),('tough',None)):
    for d in (0,1,2,3,4,5):
        res=[]
        for seed in (1,2):
            strats=dict(mk) if mk else tough(); strats['ME']=load(d)
            out=tournament_1v1(strats,MATS['S1'],seed=seed,weights={'win_rate':1/3,'cooperation':1/3,'points':1/3})
            o=sorted(out,key=lambda n:-out[n]['ptspct']); ob=sorted(out,key=lambda n:-out[n]['weighted'])
            res.append((o.index('ME')+1, ob.index('ME')+1, out['ME']['ptspct']))
        print(fname,'depth',d,'rank(points),rank(balanced),pts%:',res)
