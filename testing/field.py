# Plausible classmate strategies (4-arg signature). Mix of textbook + "Claude-written" ones.
def allc(l,m,o,meta): return 'C'
def alld(l,m,o,meta): return 'D'
def tft(l,m,o,meta): return l[0] if l else 'C'
def tf2t(l,m,o,meta):
    h=o[0]; return 'D' if len(h)>=2 and h[-1]=='D' and h[-2]=='D' else 'C'
def stft(l,m,o,meta): return l[0] if l else 'D'
def grim(l,m,o,meta): return 'D' if any('D' in h for h in o) else 'C'
def pavlov(l,m,o,meta):
    if not l: return 'C'
    return m[-1] if l[0]=='C' else ('D' if m[-1]=='C' else 'C')
def gtft(l,m,o,meta):
    if not l or l[0]=='C': return 'C'
    return 'C' if meta['rng'].random()<0.1 else 'D'
def rand(l,m,o,meta): return 'C' if meta['rng'].random()<0.5 else 'D'
def prober(l,m,o,meta):  # Detective: C D C C, then exploit if never retaliated else TFT
    r=meta['round']; seq='CDCC'
    if r<4: return seq[r]
    if 'D' not in o[0][:4]: return 'D'
    return l[0]
def endgame_tft(depth):
    def f(l,m,o,meta):
        if 200-depth<=meta['round']<200: return 'D'
        if not l: return 'C'
        return l[0]
    return f
def claude_gtft_endgame(l,m,o,meta):
    r=meta['round']; h=o[0]
    if r==199: return 'D'
    if not h: return 'C'
    if len(h)>=10 and h[-10:].count('D')>=9: return 'D'
    if h[-1]=='C': return 'C'
    if len(m)>=2 and m[-2]=='D' and h[-2]=='C': return 'C'
    return 'C' if meta['rng'].random()<0.1 else 'D'
def claude_exploiter(l,m,o,meta):
    r=meta['round']; h=o[0]
    if 198<=r<200: return 'D'
    if not h: return 'C'
    if r==5: return 'D'
    if r>7 and h[6]=='C' and h[7]=='C':
        return 'D' if r%2==0 else 'C'
    return h[-1]
def claude_adaptive(l,m,o,meta):
    r=meta['round']; h=o[0]
    if r==199: return 'D'
    if not h: return 'C'
    if r>=20:
        rate=h.count('C')/len(h)
        if rate<0.3: return 'D'
    return h[-1]
def soft_majority(l,m,o,meta):
    h=o[0]; return 'C' if h.count('C')>=h.count('D') else 'D'
def grudger_forgive(l,m,o,meta):
    h=o[0]
    if not h: return 'C'
    return 'D' if 'D' in h[-5:] else 'C'
def guide_adapts(l,m,o,meta):
    game=meta['tournament_info'].get('format')
    if not l: return 'C'
    if game=='os_simulation': return 'C' if l[0]=='D' else 'D'
    if game=='n_player': return 'C' if l.count('C')*2>=len(l) else 'D'
    return l[0]
def careful(l,m,o,meta):
    if not l: return 'C'
    if meta['n_players']>2: return 'C' if 'D' not in l else 'D'
    return l[0]
def np_threshold(th):
    def f(l,m,o,meta):
        if not l: return 'C'
        return 'C' if l.count('C')/len(l)>=th else 'D'
    return f
def np_freerider_end(l,m,o,meta):
    if meta['round']>=198: return 'D'
    if not l: return 'C'
    return 'C' if l.count('C')*2>=len(l) else 'D'

FIELD = {
 'AllC':allc,'AllD':alld,'TFT':tft,'TF2T':tf2t,'STFT':stft,'Grim':grim,'Pavlov':pavlov,'GTFT':gtft,
 'Random':rand,'Prober':prober,'TFT-end1':endgame_tft(1),'TFT-end2':endgame_tft(2),'TFT-end3':endgame_tft(3),
 'ClaudeGTFTend':claude_gtft_endgame,'ClaudeExploit':claude_exploiter,'ClaudeAdaptive':claude_adaptive,
 'SoftMaj':soft_majority,'GrudgeForgive':grudger_forgive,'GuideAdapts':guide_adapts,
 'Careful':careful,'NP-th0.5':np_threshold(0.5),'NP-th0.75':np_threshold(0.75),'NP-th1.0':np_threshold(1.0),
 'NP-freeEnd':np_freerider_end,
}
