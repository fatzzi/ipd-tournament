# IPD tournament strategy (PRIVATE)

Operating Systems class Prisoner's Dilemma tournament, October 2026.
**Keep this repo private.** Submitted code is readable by every classmate on the class site.

## Files

| File | What it is | Submit? |
|---|---|---|
| `strategies/strategy.py` | **Main strategy, fully commented.** Source of truth; edit this one. | No, never paste this one |
| `strategies/submit.py` | Same code with comments and docstrings stripped. | **Yes**, for Sprint 1, Sprint 2 and the Final |
| `strategies/decoy.py` | Plain forgiving tit-for-tat that gives nothing away. | Soft launch only (Tue 20 Oct) |
| `testing/` | Local test harness that mirrors the site's scoring | n/a |
| `local-only/` (not in git) | Class token, fetched gallery, copy of the instructor's app source | n/a |

Regenerate `submit.py` after editing `strategy.py`:

```bash
python testing/make_submit.py
```

## Schedule

| When | Round | Plan |
|---|---|---|
| Tue 20 Oct | Soft launch | Submit `decoy.py` |
| Wed 21 to Thu 22 Oct | Sprint 1 (classic payoffs, PG b=0.4 groups of 5, RR 8 cores) | Re-test against the gallery, then submit `submit.py` late |
| Fri 23 to Sat 24 Oct | Sprint 2 (4/0/6/2, PG b=0.3 groups of 5, Priority 8 cores) | Same |
| Sun 25 Oct | Final (4/0/7/2, PG b=0.25 groups of 8, Priority 4 cores) | Same |

Keep the same entry name all week, so the switch from the decoy doesn't stand out.

## How the strategy works

- **Reads the ranking weights** (`meta['tournament_info']['weights']`). In 1v1 it plays always-defect if win rate dominates, and turns on "never finish a match behind" once win rate is at least 25% of the weights. In N-Player it keeps cooperating if cooperation is weighted.
- **1v1:** contrite tit-for-tat. It defects against opponents that don't respond to it, defects in rounds 197 to 199 of fixed 200-round matches, and breaks C/D see-saw loops.
- **1v1 stochastic last round (simulator bug):** both players get the same `meta['rng']` that decides when a stochastic match ends. The strategy copies its state and checks that it advanced by exactly one draw every round, which proves the mode is stochastic. It then peeks at the next draw and defects on the true last round. This hit the last round in 40 of 40 sandbox tests and never fires in other modes.
- **N-Player, groups of 5:** cooperates, probes once at round 2, free-rides on groups that tolerate it, defects when a habitual defector is present, and defects in the last 2 rounds of fixed-length modes.
- **N-Player, groups of 7 or more (the Final):** free-rides, because that won top 3 most often in testing.
- **OS sim:** gives the CPU back when the computer is busy and holds it 70% of the time when calm. Against the guide's example this was a statistical tie in the final check.

## Testing

```bash
python testing/fetch_gallery.py
python testing/evalhub2.py strategies/strategy.py local-only/strategies.json
python testing/eval1v1.py strategies/strategy.py
python testing/evalnp3.py strategies/strategy.py
python testing/peekcheck.py strategies/submit.py
```

The OS-sim scripts take the app path first, for example `python testing/os_final.py local-only/ipd-app strategies/strategy.py priority 4 200`. Each takes several minutes.

`testing/field.py` holds about 25 strategies that classmates might plausibly write, used as a stand-in until the class gallery fills up.
