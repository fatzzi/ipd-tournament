# IPD tournament strategy (PRIVATE)

Operating Systems class Prisoner's Dilemma tournament, October 2026.
**Keep this repo private.** Submitted code is readable by every classmate on the class site.

## Files

| File | What it is | Submit? |
|---|---|---|
| `strategies/strategy.py` | **Main strategy, fully commented.** Source of truth; edit this one. | No, never paste this one |
| `strategies/submit.py` | Same code with comments and docstrings stripped. | **Yes**, for Sprint 1, Sprint 2 and the Final |
| `strategies/decoy.py` | Plain forgiving tit-for-tat that gives nothing away. | Only if you need a placeholder |
| `testing/` | Local test harness that mirrors the site's scoring | n/a |
| `local-only/` (not in git) | Class token, fetched gallery, copy of the instructor's app source | n/a |

Regenerate `submit.py` after editing `strategy.py`:

```bash
python testing/make_submit.py
```

## Rules (updated 22 Oct)

- Each round (Sprint 1, Sprint 2, Final) awards +5 to the top 3 in **each** mode (1v1, N-Player, OS), so 9 awards per round.
- **At most one +5 per student.** Past winners stay in the pool but can't win again, so the next eligible student gets it.
- Submissions lock around 11:59 on Thu 22 (Sprint 1), Sat 24 (Sprint 2) and Sun 25 Oct (Final).
- Sprint 2 and Final settings may change based on Sprint 1, so the strategy reads payoffs and weights at run time.

## Plan

Submit `strategies/submit.py` before each lock, as late as is safe. Keep the same entry name all week.
Before each lock: `python testing/fetch_gallery.py`, then rerun the tests below against the new field.

## How the strategy works (as of 22 Oct)

- **1v1:** contrite tit-for-tat. Defects against opponents that don't return cooperation (they return our C less than 60% of the time over the last 30 rounds). Defects in rounds 193 to 199 of fixed 200-round matches, because classmates start at 195.
- **1v1 stochastic last round (simulator bug):** both players get the same `meta['rng']` that decides when a stochastic match ends. The strategy checks that the generator advanced by exactly one draw every round, which proves the mode is stochastic, then peeks at the next draw and defects on the true last round. This hit the last round in 40 of 40 sandbox tests and never fires in other modes.
- **Ranking weights:** always-defect if win rate dominates. "Never finish a match behind" if win rate is at least 25% of the weights.
- **N-Player:** the site's results page ranks by weighted score (default 33% group win / 34% cooperation / 33% points), not raw points. One group match per player, so a group win is worth about 33 points, and a tie at the top counts as a draw (no win). The strategy defects until it leads every rival by 4 cooperations, then cooperates. If a rival defects as much as we do (a pure defector), the win is out of reach, so it cooperates fully. In discounted mode it cooperates as soon as no rival can catch up, because late rounds are worth almost no points but count fully for cooperation. It free-rides only if points are at least 80% of the weights. Missing weights are treated as the site default 33/34/33.
- **OS sim:** the guide's rule, plus give the CPU back if the *previous* signal was also busy (`OS_LOOKBACK = 1`). In Sprint 1 settings (seeds 1-30) it beat the guide's rule, which 8 classmates submit, in 15 of 21 ten-seed windows (mean 4.206 vs 4.232). Through the site's scoring it won on 3 of 3 seeds. Adaptive Yield uses a 2-signal lookback (4.197 mean, 14/21); head to head we're even.

## Results against the real class gallery (22 Oct afternoon, 20 entries, ranked among students only)

- 1v1, equal weights: rank 1 or 2 in 8 of 8 seeds. Points-only: a near-tie of about 6 entries within 1%, top 3 in 1 of 8.
- N-Player, Sprint 1 settings, weighted ranking, real engine: top 3 in 11 of 30 shuffles (mean rank 5.1). Always-defect: 9/30 (mean 7.9). The previous version: 1/30.
- OS: seed 1 through the site's scoring: us 4.19, Adaptive Yield 4.21, the guide's rule 4.23 (8 entries tied). Top 3 in 16 of 21 ten-seed windows.

## Testing

```bash
python testing/fetch_gallery.py
python testing/eval_real.py strategies/strategy.py S1
python testing/np_real.py strategies/strategy.py
python testing/os_report.py round_robin_8_100
python testing/eval1v1.py strategies/strategy.py
python testing/evalnp3.py strategies/strategy.py
python testing/peekcheck.py strategies/submit.py
```

The OS-sim scripts take the app path first, for example `python testing/os_final.py local-only/ipd-app strategies/strategy.py priority 4 200`. Each takes several minutes.

`testing/field.py` holds about 25 strategies that classmates might plausibly write, used as a stand-in until the class gallery fills up.
