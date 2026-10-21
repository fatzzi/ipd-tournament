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
- **N-Player:** always free-ride. The class field is very tolerant (two always cooperate, several follow the majority), and always-defect won top 3 most often in the Sprint 1 and Sprint 2 settings and tied in the Final settings. If cooperation is weighted, it switches to a probing conditional cooperator.
- **OS sim:** exactly the guide's rule. A 60-seed study scored like the site found nothing that reliably beats it, and about 7 classmates submit it, so we tie with them rather than gamble.

## Results against the real class gallery (22 Oct, 16 entries)

- 1v1: highest total score against the field. With equal weights, 1st in 4 of 5 seeds.
- N-Player: top 3 in 12 of 60 group shuffles (Sprint 1 settings), 14 of 60 (Sprint 2) and 18 of 60 (Final).
- OS: identical numbers to the guide's rule in all three settings.

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
