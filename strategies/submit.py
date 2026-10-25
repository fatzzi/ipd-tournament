def sentinel(last_moves, my_history, opponents_histories, meta):
 try:
  return _brain((last_moves, my_history, opponents_histories, meta))
 except Exception:
  return last_moves[0] if last_moves else 'C'

def _brain(ctx):
 last_moves, my_history, opponents_histories, meta = ctx
 info = meta.get('tournament_info') or {}
 fmt = info.get('format', '2-player')
 rnd = meta.get('round', len(my_history))
 me = my_history
 w = info.get('weights') or {}
 try:
  ww, wc, wp = (float(w.get(k) or 0) for k in ('win_rate', 'cooperation', 'points'))
 except (TypeError, ValueError, AttributeError):
  ww = wc = wp = 0.0
 if ww + wc + wp <= 0:
  ww, wc, wp = (0.33, 0.34, 0.33)
 FIXED_LENGTH = 200
 ENDGAME_1V1 = 12 if ww > 0 else 1
 END_MODES = ('standard',)
 POINTS_ONLY_NP = 0.8
 NP_TARGET = 1.0
 ENDGAME_NP = 10
 OS_LOOKBACK = 7
 OS_MIN_BUSY = 2
 RESPONSIVE_WINDOW = 30
 RETURN_MIN = 0.6
 WIN_SHARE = 0.25
 EXPLOIT_PD = 0.8
 if fmt == 'os_simulation':
  if not last_moves or last_moves[0] == 'D':
   return 'C'
  past = opponents_histories[0] if opponents_histories else []
  if OS_LOOKBACK and past[-OS_LOOKBACK:].count('D') >= OS_MIN_BUSY:
   return 'C'
  return 'D'
 if fmt == 'n_player':
  if wp / (ww + wc + wp) >= POINTS_ONLY_NP:
   return 'D'
  if not opponents_histories:
   return 'C'
  pm = info.get('payoff_model') or {}
  b, c = (float(pm.get('b', 0.3) or 0), float(pm.get('c', 1) or 1))
  cap = max(b * (len(opponents_histories) + 1) - c, 0.01)
  if info.get('mode') in ('standard', 'discounted') and FIXED_LENGTH - ENDGAME_NP <= rnd < FIXED_LENGTH:
   return 'D'
  if rnd == 0 or wc >= wp * (c - b) / cap:
   return 'C'
  lo = max(0, rnd - 20)
  k = sum((h[t] == 'C' for h in opponents_histories for t in range(lo, rnd))) / (rnd - lo)
  x = max(0.0, min(1.0, (b * k - cap) / (c - b)))
  mix = wc * x + wp * max(0.0, min(1.0, (b * k - (c - b) * x) / cap))
  if wc + wp * max(0.0, min(1.0, (b * k + b - c) / cap)) > mix:
   return 'C'
  got = sum((b * (sum((h[t] == 'C' for h in opponents_histories)) + (me[t] == 'C')) - c * (me[t] == 'C') for t in range(rnd)))
  return 'C' if got / rnd >= cap * NP_TARGET - 1e-09 else 'D'
 if 0.95 * ww + 0.3 * wp > 0.75 * ww + 0.9 * wc + 0.58 * wp:
  return 'D'
 opp = opponents_histories[0] if opponents_histories else []
 if not opp:
  return 'C'
 n = len(opp)
 pm = info.get('payoff_matrix') or {'CC': [3, 3], 'CD': [0, 5], 'DC': [5, 0], 'DD': [1, 1]}
 greedy = wp * (pm['DC'][0] - pm['CC'][0]) / max((v[0] for v in pm.values())) > wc
 if info.get('mode', 'standard') in END_MODES and FIXED_LENGTH - ENDGAME_1V1 <= rnd < FIXED_LENGTH:
  return 'D'
 if ww > 0 and ww / max(ww + wc + wp, 1e-09) >= WIN_SHARE:
  diff = sum((pm[a + b][0] - pm[a + b][1] for a, b in zip(me, opp)))
  if diff < 0:
   return 'D'
 if n >= 20:
  lo = max(0, n - 1 - RESPONSIVE_WINDOW)
  after_c = [opp[t + 1] for t in range(lo, n - 1) if me[t] == 'C']
  after_d = [opp[t + 1] for t in range(lo, n - 1) if me[t] == 'D']
  if greedy and len(after_d) >= 5 and (after_d.count('C') / len(after_d) >= EXPLOIT_PD):
   return 'D'
  if len(after_c) >= 5 and len(after_d) >= 5:
   pc = after_c.count('C') / len(after_c)
   pd = after_d.count('C') / len(after_d)
   if pc - pd < 0.2 and pc < 0.8 or pc < RETURN_MIN:
    return 'D'
 if opp[-1] == 'C':
  return 'C'
 if n >= 2 and me[-2] == 'D' and (opp[-2] == 'C') and (me[-1] == 'C'):
  return 'C'
 if n >= 2 and me[-2] == 'D':
  j = n - 2
  while j > 0 and me[j - 1] == 'D':
   j -= 1
  if j >= 1 and opp[j - 1] == 'C' and (opp[j] == 'C'):
   return 'C'
 run = 0
 for t in range(n - 1, -1, -1):
  if opp[t] == 'D' and me[t] == 'D':
   run += 1
  else:
   break
 if run >= 3 and opp.count('C') * 2 > n and (run % 4 == 3):
  return 'C'
 return 'D'
