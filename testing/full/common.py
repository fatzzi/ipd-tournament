import sys, json
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\testing')
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\local-only\ipd-app')
# Last gallery with visible code (22 Oct 23:37, 39 entries; code is hidden from then on).
GAL = r'C:\Users\fxtim\Desktop\ipd-tournament\local-only\gallery_snapshot_2026-10-22_2337.json'
BOTS = {'multiplicative_update', "Claude's_strategy", 'multiplicative_update_merciful', 'probabilistic_expectation', 'Salman', "Hijab's strategy"}
def tag(n): return n + (' (bot)' if n in BOTS else '') + ('   <-- US' if n == 'yay' else '')
