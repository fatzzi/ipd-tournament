# Mirrors app.game / round_robin_tournament / determine_weighted_results and
# n_player_simulation.group_tournament scoring (no sandbox, for speed).
import random, itertools
MATS = {'S1':{'CC':[3,3],'CD':[0,5],'DC':[5,0],'DD':[1,1]},
        'S2':{'CC':[4,4],'CD':[0,6],'DC':[6,0],'DD':[2,2]},
        'F' :{'CC':[4,4],'CD':[0,7],'DC':[7,0],'DD':[2,2]}}
MODES=['standard','discounted','stochastic','random']

def game(fa,fb,mat,mode,R,seed,ti):
    rng=random.Random(seed); ha=[];hb=[]; wa=wb=tw=0; ra=rb=0; ca=cb=0; r=0
    lim = R if mode=='random' else 200
    while True:
        if mode=='stochastic':
            if r>0 and rng.random()>0.995: break
            if r>=2000: break
        elif r>=lim: break
        ma=fa([hb[-1]] if hb else [],ha[:],[hb[:]],{'round':r,'n_players':2,'player_index':0,'tournament_info':ti,'rng':rng})
        mb=fb([ha[-1]] if ha else [],hb[:],[ha[:]],{'round':r,'n_players':2,'player_index':1,'tournament_info':ti,'rng':rng})
        assert ma in ('C','D') and mb in ('C','D')
        pa,pb=mat[ma+mb]; w=0.95**r if mode=='discounted' else 1
        wa+=pa*w; wb+=pb*w; tw+=w; ra+=pa; rb+=pb; ca+=ma=='C'; cb+=mb=='C'
        ha.append(ma); hb.append(mb); r+=1
    return wa/tw, wb/tw, ra, rb, ca, cb, r

def tournament_1v1(strats, mat, seed=1, weights=None):
    weights = weights or {'win_rate':0,'cooperation':0,'points':1}
    ti={'weights':weights,'payoff_matrix':mat,'format':'2-player','n_players':2,'payoff_model':'standard'}
    R=random.Random(seed).randint(100,300)
    names=sorted(strats); st={n:dict(tp=0,raw=0,moves=0,coop=0,w=0,d=0,l=0) for n in names}
    for i,(a,b) in enumerate(itertools.combinations(names,2)):
        pa=pb=0
        for mi,mode in enumerate(MODES):
            sa,sb,ra,rb,ca,cb,r=game(strats[a],strats[b],mat,mode,R,seed+i*1000+mi,ti)
            pa+=sa; pb+=sb; st[a]['raw']+=ra; st[b]['raw']+=rb; st[a]['moves']+=r; st[b]['moves']+=r
            st[a]['coop']+=ca; st[b]['coop']+=cb
        st[a]['tp']+=pa/4; st[b]['tp']+=pb/4
        if pa>pb: st[a]['w']+=1; st[b]['l']+=1
        elif pb>pa: st[b]['w']+=1; st[a]['l']+=1
        else: st[a]['d']+=1; st[b]['d']+=1
    mx=max(v[0] for v in mat.values()); out={}
    for n,s in st.items():
        g=s['w']+s['d']+s['l']
        o=dict(points=s['tp'], ptspct=s['raw']/s['moves']/mx, win=s['w']/g, coop=s['coop']/s['moves'])
        o['weighted']=o['win']*weights.get('win_rate',0)+o['coop']*weights.get('cooperation',0)+o['ptspct']*weights.get('points',0)
        out[n]=o
    return out

def game_n(fs,b,mode,R,seed):
    n=len(fs); rng=random.Random(seed); H=[[] for _ in fs]; tot=[0]*n
    lim=R if mode=='random' else (2000 if mode=='stochastic' else 200)
    for r in range(lim):
        if mode=='stochastic' and r>0 and rng.random()>0.995: break
        mv=[]
        for p in range(n):
            opp=[i for i in range(n) if i!=p]
            ti={'format':'n_player','mode':mode,'modes':MODES,'n_players':n}
            mv.append(fs[p]([H[i][-1] for i in opp] if r else [],H[p][:],[H[i][:] for i in opp],
                            {'round':r,'n_players':n,'player_index':p,'tournament_info':ti,'rng':rng}))
        k=mv.count('C'); w=0.95**r if mode=='discounted' else 1
        for p in range(n): tot[p]+=(b*k-(1 if mv[p]=='C' else 0))*w; H[p].append(mv[p])
    return tot

def tournament_np(strats,b,gsize,seed=1,modes=MODES):
    names=sorted(strats); rng=random.Random(seed); idx=list(range(len(names))); rng.shuffle(idx)
    groups=[idx[i:i+gsize] for i in range(0,len(idx),gsize)]
    if len(groups)>1 and len(groups[-1])==1: groups[-2].extend(groups.pop())
    R=random.Random(seed).randint(100,300); pts={}
    for gi,g in enumerate(groups):
        acc=[0]*len(g)
        for mi,mode in enumerate(modes):
            t=game_n([strats[names[i]] for i in g],b,mode,R,seed+gi*10000+mi)
            acc=[a+x for a,x in zip(acc,t)]
        for j,i in enumerate(g): pts[names[i]]=acc[j]/len(modes)
    return pts
