# Sprint 1 — official results (published 23 Oct 2026, fetched 24 Oct)

Raw data (read-only GETs) is in `local-only/results/` (gitignored): `1v1_*.json`, `nplayer_*.json`,
`os_*.json`, plus `snapshot_d88ALQsdiP9W10XTQmvD.json` = **all 66 Sprint-1 submissions with code**.
Fetch again with `python testing/fetch_results_api.py`.

## Our finishes (entry `yay`, 65 ranked in each game)
| Game | Our rank | Our score | Podium | Gap to 3rd |
|---|---|---|---|---|
| 1v1 (total points) | **9th** | 182.37 | AMK30496 184.23 · Taha's Strategy 184.04 · losttttttttttt 183.78 | 1.41 pts |
| N-Player (total points) | **52nd** | 0.00 (draw) | kk 168.40 · then four at 63.15 | — |
| OS (avg response, lower better) | **13th** | 4.16 | akash_alam 4.10 · Shahzaib Fareed 4.10 · Fable 4.10 | 0.06 |

No +5 this round. Sprint 1 earned the +3 bug-report credit only.

## What the results teach
- **The real field was unseen.** 66 submissions; the 22 Oct snapshot we tuned on was mostly
  replaced (`butt_sahab` never entered). Local "top 3 vs the snapshot" did not transfer.
- **1v1:** the pack is tight (1st–20th = 184.23 → 181.08). We went 22W/10D/32L at 91% coop; the
  podium wins far more matches (AMK30496 47W, Taha 48W) at the same points. We are a little too
  forgiving and get edged in close matches.
- **N-Player:** always-defect is all-or-nothing — 0 points when your group has no cooperators to
  free-ride on (ours didn't). Groups are one match each, so luck dominates.
- **OS:** the top 7 all tie at 4.10 (times stored to 2 decimals) and split on waiting time. Every
  one of them yields when the CPU was busy in **any of the last 4–8 signals** (akash_alam 5,
  Shahzaib 5, Fable 8, yoyo_final/KT_VF 4). We looked back only 1. Official run: round robin,
  8 cores, 100 processes, 10 runs, all four workloads (Uniform/Poisson/Mixed/Bursty), seed 29257.
  Our earlier local study pointed the other way, so something in that setup differed from the
  official run — check before trusting it again.

## Sprint 2 status (site, 24 Oct)
"Happening now" Sat 24 – Sun 25 Oct. Payoffs, discount factor, stochastic chance and ranking
weights all say **"To be released"**. The strategy reads them from `meta` at runtime.

## Next
1. Validate the harness: replay the official Sprint-1 1v1 / OS with the 66-strategy snapshot and
   check we reproduce the published order. Only then tune on it.
2. Retune for Sprint 2 against the real field + archetypes (not one snapshot): longer OS
   look-back (Priority scheduler in Sprint 2), a slightly harder 1v1, a less all-or-nothing
   N-Player.
