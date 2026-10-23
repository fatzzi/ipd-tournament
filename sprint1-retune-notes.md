# Sprint 1 — 1v1 points-only retune (23 Oct 2026, overnight)

Sprint 1 locks **Fri 23 Oct 11:59 pm**. Ranking is **total points only** (weights points 1.0)
for 1v1 and N-Player; OS is average response time. Nothing here was submitted or committed —
all local, ready for you to resubmit with app **v1.4.0** before the lock.

## What changed
`strategies/strategy.py`, one line — the 1v1 endgame is now **weight-aware**:

```python
ENDGAME_1V1 = 7 if ww > 0 else 1
```

- **Points-only (Sprint 1): defect only on the last round (199).** A longer endgame secures
  *match wins* but, with no win-rate weight, it just triggers retaliation from the many
  reciprocators in the field and bleeds points.
- **Win-rate weighted (default / likely Sprint 2-Final): keeps the old 7-round endgame**, so
  our previous equal-weights dominance is untouched. The change can't silently regress later.

`strategies/submit.py` regenerated (3453 bytes, URL 6199 chars < 7500, passes `is_safe_code`,
behaviour identical to `strategy.py`). OS and N-Player code paths are unchanged.

## Results (exact-seed harness `testing/v1_sweep.py`, 8 seeds, 22 Oct 23:37 snapshot field)
| | points-only mean | points-only student ranks | top3 | equal-weights ranks | top3 |
|---|---|---|---|---|---|
| Baseline (end 7)   | 0.5440 | [9, 23, 7, 22, 9, 16, 16, 11] | 0/8 | [1, 2, 1, 3, 1, 2, 1, 1] | 8/8 |
| **Retuned (end 1)**| **0.5462** | **[7, 23, 5, 21, 4, 11, 14, 9]** | 0/8 | [1, 2, 1, 3, 1, 2, 1, 1] | 8/8 |

Mean 1v1 student rank on points improved ~14.1 → ~11.8; equal-weights dominance preserved.

## Honest read
- 1v1 points-only is a **tight pack** (top ~20 within ~2.5 pts). The improvement is real but
  **not a lock for top 3** — we land roughly rank 4–11 depending on the tournament seed.
- The visible leader `butt_sahab` (56.4) wins partly by **fingerprinting specific classmates**
  (e.g. pre-empting Ferozis at round 194). That is fragile against the TA's hidden baselines
  and against your "don't leak / don't overfit" rule, so it was deliberately not copied.
- **OS is still our realistic medal** (1st locally, 4.19). N-Player is pure always-defect under
  points-only (the points-max), ~5/30 top-3.

## Tried and rejected (clean harness)
- **Generosity (GTFT-style forgiveness):** looked like a win (+0.3 pts) only because the first
  version drew from `meta['rng']`, which perturbs the shared stochastic-continuation stream —
  an artifact. A clean round-based version is **neutral on the snapshot and actively worse once
  baselines/exploiters are added** (forgiveness just leaks cooperation). Dropped.
- **Cooperation-rate cutoff (all-D vs opp coop < 45%):** clearly worse (defects on moderate
  cooperators, loses CC). Dropped.
- **Responsiveness detector on/off, narrow/wide window, RETURN_MIN:** neutral; left as-is.

## N-Player note (optional, not applied)
Under points-only + the cooperation-% tiebreak, seeding 2 cooperative rounds (`D+coop2`) nudged
pts% 29.4→31.7 and top3 5→6 /30, but mean rank got *worse* (14.8→16.0) — a noisy wash. Left as
pure always-defect. Flagging only in case you want to gamble on it for N-Player.

## New / updated test scripts (local, not committed)
- `testing/v1_retune.py` — fast exact points-only sweep (opp-vs-opp cached per seed; `+base`
  adds classic baselines as an anti-overfit proxy).
- `testing/v1_policies.py` — direct 1v1 policy search. NOTE its simplified `endgame` defects at
  every round ≥199, which is wrong in stochastic matches; trust `v1_retune` / `v1_sweep` instead.
- `testing/np_points.py` — N-Player real-engine points-only ranking with the coop-% tiebreak.

## To resubmit (you do this — I don't submit or sign in)
1. Open app **v1.4.0** (old versions are refused by the site).
2. Submit `strategies/submit.py` as entry **yay** before 11:59 pm. (Resubmitting moves us later
   in the tie-break, but points come first, so it's worth it.)
