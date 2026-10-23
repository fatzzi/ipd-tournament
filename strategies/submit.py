import random

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
 ENDGAME_1V1 = 7 if ww > 0 else 1
 LEAD_NP = 4
 HOPELESS_NP = 5
 POINTS_ONLY_NP = 0.8
 OS_LOOKBACK = 1
 RESPONSIVE_WINDOW = 30
 RETURN_MIN = 0.6
 WIN_SHARE = 0.25
 EXPLOIT_PD = 0.8
 if fmt == 'os_simulation':
  if not last_moves or last_moves[0] == 'D':
   return 'C'
  past = opponents_histories[0] if opponents_histories else []
  if OS_LOOKBACK and 'D' in past[-OS_LOOKBACK:]:
   return 'C'
  return 'D'
 if fmt == 'n_player':
  if wp / (ww + wc + wp) >= POINTS_ONLY_NP:
   return 'D'
  if not opponents_histories or rnd == 0:
   return 'D'
  my_c = me.count('C')
  if rnd >= HOPELESS_NP:
   for h in opponents_histories:
    if h.count('C') <= my_c and 'C' not in h[-HOPELESS_NP:]:
     return 'C'
  disc = info.get('mode') == 'discounted'
  df = float(info.get('discount_factor') or 0.95) if disc else 1.0
  wts = [df ** t for t in range(len(me))]
  mine = sum((x for x, m in zip(wts, me) if m == 'C'))
  lead = min((sum((x for x, m in zip(wts, h) if m == 'C')) for h in opponents_histories)) - mine
  need = LEAD_NP
  if disc and df < 1:
   need = min(LEAD_NP, df ** rnd / (1 - df) + 0.5)
  return 'C' if lead >= need else 'D'
 if 0.95 * ww + 0.3 * wp > 0.75 * ww + 0.9 * wc + 0.58 * wp:
  return 'D'
 stochastic = False
 try:
  state = meta['rng'].getstate()
  me_fn = sentinel
  if rnd == 0:
   me_fn.prev_state, me_fn.one_draw_rounds = (state, 0)
  else:
   probe = random.Random()
   probe.setstate(me_fn.prev_state)
   probe.random()
   if probe.getstate() == state:
    me_fn.one_draw_rounds += 1
   else:
    me_fn.one_draw_rounds = -10 ** 6
   me_fn.prev_state = state
   if me_fn.one_draw_rounds == rnd and rnd >= 3:
    stochastic = True
 except Exception:
  stochastic = False
 opp = opponents_histories[0] if opponents_histories else []
 if not opp:
  return 'C'
 n = len(opp)
 if not stochastic and FIXED_LENGTH - ENDGAME_1V1 <= rnd < FIXED_LENGTH:
  return 'D'
 if ww > 0 and ww / max(ww + wc + wp, 1e-09) >= WIN_SHARE:
  pm = info.get('payoff_matrix') or {'CC': [3, 3], 'CD': [0, 5], 'DC': [5, 0], 'DD': [1, 1]}
  diff = sum((pm[a + b][0] - pm[a + b][1] for a, b in zip(me, opp)))
  if diff < 0:
   return 'D'
 if n >= 20:
  lo = max(0, n - 1 - RESPONSIVE_WINDOW)
  after_c = [opp[t + 1] for t in range(lo, n - 1) if me[t] == 'C']
  after_d = [opp[t + 1] for t in range(lo, n - 1) if me[t] == 'D']
  if len(after_d) >= 5 and after_d.count('C') / len(after_d) >= EXPLOIT_PD:
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
