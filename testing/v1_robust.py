# Anti-overfit validation for the 1v1 points-only strategy.
# (a) Head-to-head diagnostics vs novel archetypes NOT in the snapshot: our avg payoff/round and
#     the opponent's coop%, so we can see we cooperate with reciprocators (~3), defend against
#     defectors (~1), harvest pushovers (>3), and -- critically -- do NOT misfire the exploit rule
#     on noisy/generous reciprocators (which would collapse us into DD spirals).
# (b) Field-rank on fields that are NOT the tuning snapshot (baselines-only; novel-synthetic-only).
import sys, random, statistics
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
from hubfield import load_hub
from sim import game, MATS, MODES
import field as F

MAT = MATS['S1']; TI = {'weights': {'points': 1}, 'payoff_matrix': MAT, 'format': '2-player', 'n_players': 2, 'payoff_model': 'standard'}
g = {}; exec(open(r'C:\Users\fxtim\Desktop\ipd-tournament\strategies\strategy.py', encoding='utf-8').read(), g)
OURS = g['sentinel']

# ---- novel archetypes future classmates might submit (none are in the snapshot) ----
def noisy_tft(p):
    def f(l, m, o, meta):
        h = o[0] if o else []; base = h[-1] if h else 'C'
        if meta['rng'].random() < p: return 'D' if base == 'C' else 'C'
        return base
    return f
def gtft(gp):
    def f(l, m, o, meta):
        h = o[0] if o else []
        if not h or h[-1] == 'C': return 'C'
        return 'C' if meta['rng'].random() < gp else 'D'
    return f
def nice_then_alld(k):
    def f(l, m, o, meta): return 'D' if meta.get('round', len(m)) >= k else 'C'
    return f
def patient_grudger(tol):
    # tolerate defections for the first `tol` rounds; after that, if opp ever defected, all-D forever.
    def f(l, m, o, meta):
        h = o[0] if o else []; r = meta.get('round', len(m))
        if r < tol: return l[0] if l else 'C'
        return 'D' if 'D' in h else 'C'
    return f
def extort(l, m, o, meta):  # simplified ZD-extortion-ish: mostly D, reward only sustained C
    h = o[0] if o else []
    if not h: return 'C'
    if len(h) >= 2 and h[-1] == 'C' and h[-2] == 'C': return 'C' if meta['rng'].random() < 0.4 else 'D'
    return 'D'
def contrite(l, m, o, meta):
    h = o[0] if o else []
    if not h: return 'C'
    if h[-1] == 'C': return 'C'
    if len(m) >= 2 and m[-2] == 'D' and h[-2] == 'C': return 'C'
    return 'D'
def randp(p):
    def f(l, m, o, meta): return 'C' if meta['rng'].random() < p else 'D'
    return f

ARCH = {
    'AllC': F.allc, 'AllD': F.alld, 'TFT': F.tft, 'STFT': F.stft, 'TF2T': F.tf2t, 'Grim': F.grim,
    'Pavlov': F.pavlov, 'GTFT.1': gtft(0.1), 'GTFT.3': gtft(0.3), 'NoisyTFT.05': noisy_tft(0.05),
    'NoisyTFT.15': noisy_tft(0.15), 'Gradual': None, 'Contrite': contrite, 'Prober': F.prober,
    'Extort': extort, 'PatientGrudger20': patient_grudger(20), 'Nice->D@150': nice_then_alld(150),
    'Nice->D@100': nice_then_alld(100), 'Rand.7': randp(0.7), 'Rand.5': randp(0.5), 'SoftMaj': F.soft_majority,
    'GrudgeForgive': F.grudger_forgive,
}
del ARCH['Gradual']  # (Gradual lives in v1_policies; skip to keep this self-contained)

def duel(me, opp, seeds=6):
    ours = []; oppc = []
    for s in range(1, seeds + 1):
        R = random.Random(s).randint(100, 300)
        for mi, mode in enumerate(MODES):
            _, _, ra, rb, ca, cb, r = game(me, opp, MAT, mode, R, s * 17 + mi, TI)
            ours.append(ra / r); oppc.append(cb / r * 100)
    return statistics.mean(ours), statistics.mean(oppc)

print('== Head-to-head: OURS vs novel archetypes (not in snapshot) ==')
print(f'{"archetype":18s} {"ourPts/rnd":>10s} {"oppCoop%":>9s}   verdict')
flags = []
for an, af in ARCH.items():
    op, oc = duel(OURS, af)
    # classify: reciprocators/cooperators should give us ~3 (we sustain CC). A misfire shows up as
    # us scoring << 2.5 against a FRIENDLY opponent (we wrongly defected -> DD spiral).
    friendly = oc >= 55
    verdict = 'exploit/defend' if op >= 3.3 or oc < 40 else ('OK (CC)' if op >= 2.7 else 'LOW!')
    if friendly and op < 2.6:
        verdict += '  <-- possible misfire'; flags.append(an)
    print(f'{an:18s} {op:10.2f} {oc:9.1f}   {verdict}')
print('\nmisfire flags:', flags or 'none')
