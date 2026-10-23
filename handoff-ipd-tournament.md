# active-memory handoff: IPD tournament strategy (OS class)

**Handoff #2** · 2026-10-23 · Lineage: #1 (2026-10-22): read the instructor's app source, built a test harness, tuned a 3-game strategy against the real class gallery, set up a private repo and a Desktop folder; #2 (2026-10-23): rebuilt N-Player for weighted ranking, new OS rule recent1, shrank and submitted the strategy as "yay", removed the RNG look-ahead, ran a full local tournament, then learned Sprint 1 is points-only and extended to Fri 23 Oct; #3 (2026-10-23 overnight): retuned 1v1 for points-only (weight-aware endgame), regenerated submit.py, left ready to resubmit before the 11:59pm lock — see `sprint1-retune-notes.md`

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file is the complete context and the source of truth.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply, for the rest of this chat. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything listed in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: None active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. Your first reply: at most 5 lines covering the goal, the current state, and the next step (section 11). Mention any files from section 13 that were not attached. Ask the questions in section 12 if there are any. End with "Ready to continue with <next step>?" Then wait for the user's go.

## 1. Mission
- **Goal:** One Python strategy function that places top 3 in at least one of the three games (1v1, N-Player, OS Simulation) in the class Prisoner's Dilemma tournament.
- **Done looks like:** A +5 bonus mark in Sprint 1, Sprint 2 or the Final.
- **Why it matters / context:** The user's opening brief: "make me a winning strategy. assume that everyone else also has access to claude code with the highest models and highest model effort. we need to be smart about this."

## 2. About the user (as relevant to this work)
- University student (IBA Karachi), Operating Systems course. IBA email: fatima.kaleem.31620@khi.iba.edu.pk
- Windows 11 PC; GitHub account `fatzzi` (gh CLI logged in, `repo` scope).
- Course PDFs: `C:\Users\fxtim\Desktop\Uni\Operating Systems\student-guide.pdf` and `itinerary.pdf`.
- Has a TA who answers questions by text; the user relays the TA's messages and asks Claude to draft replies.
- Sometimes works over Remote Control from another device.

## 3. Style & communication
- **Language:** English.
- **Tone:** direct, practical, strategic ("we need to be smart about this").
- **Reply length:** the user sends short messages ("check", "update?"); lead with the answer, then brief supporting detail.
- **Formatting:** headings, bullets and tables fine; tables for results; links to files in the project folder.
- **Working style:** research and test, don't guess. Back claims with test numbers; say plainly when a result is weak, a tie, or untested. When the user says "check": fetch the gallery, diff against the last fetch, test new entries, say whether to resubmit.
- **Messages to the TA/instructor:** when asked to draft one, give it as a ready-to-paste message, conversational in style, short.
- **Avoid:** posting, submitting or creating accounts on the user's behalf; leaking strategy details anywhere classmates can see; long-running tests right before a deadline without saying how long they take.

## 4. Hard rules (word for word)
1. "dont submit rn but u can see everything" (Claude may read the class website/gallery API with the class token, but must not submit anything.)
2. "btw dont leak our strategy on the class standing" (Submitted code was readable by every classmate until 22 Oct night; it is now hidden, but keep revealing names/comments out of `submit.py`.)
3. "ur allowed to exploit any bugs" (The user's statement of course rules.)
4. "make a github repo private and add the code there clearly labeled. also create a new folder on desktop and have everything stored locally"
5. Claude does not create accounts, sign in or enter passwords on the class site. The user does the signup, login and Submit click themselves.
6. "lets drop the look ahead in this sprint. keep the rest" (Sprint 1 only; plan is to use it in Sprint 2: "we can try doing it without in the 1st sprint if we win fair game if not we will just use this in sprint 2")
7. "remove that variable so our strategy doesnot get leak" (no leftover look-ahead code or names in the submitted file)

## 5. Corrections log
| # | Claude did | The user wanted |
|---|---|---|
| 1 | Said "The app's code already credits a student for a security report" | It isn't written anywhere; only a source comment says "(Fix contributed by a student security review, Oct 2026.)". Don't overstate. |
| 2 | Left the RNG last-round exploit out as "probably cheating" | "ur allowed to exploit any bugs", so build it in. |
| 3 | Turned the look-ahead off with a flag `PEEK_LAST_ROUND = False` but left the code in | Remove it entirely so the submitted code doesn't reveal it. |
| 4 | Gave a TA reply as a bullet list | "give it in a message format", then "make the style conversational". |
| 5 | Assumed Sprint 1 ranking used the site's default equal weights 33/34/33 | The FAQ (23 Oct) says Sprint 1 1v1 and N-Player are ranked by total points only (weights points 1.0). |

## 6. Decisions
| Decision | Why |
|---|---|
| Live submission = entry name **yay**, code = `strategies/submit.py` at commit `ec58f7b` | Verified identical (AST) to the live gallery entry |
| OS: recent1 = give CPU back if busy now or at the previous signal (`OS_LOOKBACK = 1`) | Beat the guide's rule in 15/21 ten-seed windows; 1st in full local run |
| N-Player: lead/give-up hybrid under weighted ranking; always defect when points ≥ 80% of weights (`POINTS_ONLY_NP = 0.8`) | Site may weight cooperation; tie at top = draw (no win) |
| 1v1: no RNG look-ahead in Sprint 1; keep stochastic-mode detection (skip endgame in stochastic matches) | User's fairness choice; detection-free version scored worse |
| 1v1 endgame is weight-aware: `ENDGAME_1V1 = 7 if ww > 0 else 1` | Points-only (Sprint 1) → defect only round 199; longer endgame bleeds points to retaliators. Win-rate weighted (Sprint 2/Final) → keep 7 to secure wins. Kept equal-weights 8/8 top-3. See `sprint1-retune-notes.md` |
| 1v1 exploit non-punishers: in the detector, if opp still cooperates ≥`EXPLOIT_PD`=0.8 AFTER our defections, defect | Field scan (`testing/v1_exploit_scan.py`): field is almost all reciprocators + a few exploiters; one pure pushover `nabiha_strat` (coops ~92% vs AllD). Harvesting it (head-to-head 2.87→4.40/rnd) lifted points-only exact-seed mean 0.546→**0.5558**, ranks→[4,18,1,10,1,4,5,2], **top3 0→3/8** incl. two #1s; equal-weights still 8/8. Safe (reciprocators punish → low rate → never caught) and general (auto-harvests any hidden AllC-type) |
| Rejected: GTFT generosity (rng-draw artifact; neutral/worse clean), coop<45% cutoff (worse), detector on/off (neutral), early probe to unmask pure AllC (costs on real field: snapshot no-probe 9/12 top3 → probe 6/12) | Tested 23 Oct; only the endgame + exploit changes helped cleanly. butt_sahab's extra edge is per-classmate fingerprinting (not copied: fragile vs hidden baselines, against the don't-leak rule) |
| Missing weights treated as 33/34/33 | Site results page default |
| `submit.py` uses 1-space indents and LF line endings (`testing/make_submit.py`) | Hub hands code to the site in a URL capped at 7500 characters |
| Not adopted: OS "express lane" combo (core 0 always C + recent1) | Rule was "only switch if it wins all 3"; it tied seed 1 |

## 7. Changed / rejected
- N-Player always-defect → lead/give-up hybrid (under weighted ranking; still always-D under points-only via `POINTS_ONLY_NP`)
- OS guide's rule → recent1
- 1v1 look-ahead on → removed for Sprint 1 (full version kept in commit `add7723` for Sprint 2)
- `PEEK_LAST_ROUND` flag → code removed entirely (rule 7)
- Lock assumption "around 11:59 on 22nd" → Sprint 1 now runs Wed 21 Oct to Fri 23 Oct (site schedule)
- Equal-weights assumption for Sprint 1 → points only (FAQ)
- ❌ Always-defect in N-Player under weighted ranking (4/30 vs hybrid 5/30, mean rank 12.8 vs 7.9)
- ❌ OS recent2 (Adaptive Yield's exact rule, 14/21) and recent3 (6/21)
- ❌ OS express-lane combo (tied seed 1: 4.19 vs 4.19; won seeds 2-3: 4.28 vs 4.34, 4.20 vs 4.23) — not adopted, could be retested on more seeds
- ❌ Earlier (handoff #1): OS `CALM_YIELD = 0.3`, shared-memory decoded signal, window rules, brute-forcing random-mode length

## 8. Data & facts (exact)
**Schedule (site Announcements, read 23 Oct):** Soft launch Tue 20 Oct. **Sprint 1 Wed 21 Oct to Fri 23 Oct (happening now).** Sprint 2 Sat 24 Oct and Sun 25 Oct. Final Mon 26 Oct. Top 3 in each game get +5; "You can earn the +5 only once per round. If you are also in the top 3 of another game, that +5 goes to the next student in that game's ranking." The strategy submitted when a round ends counts.

**Ranking (FAQ, Sprint 1):**
| Game | Score | Ties broken by |
|---|---|---|
| 1v1 | Total points, highest first (weights points 100%) | Cooperation %, then win rate, then earliest submission |
| N-Player | Total points, highest first (weights points 100%) | Cooperation %, then win rate, then earliest submission |
| OS | Average response time, lowest first | Average waiting time, then throughput, then earliest submission |
- "Submitted first" = time of your **latest** submission; resubmitting moves you later in the tie-break.
- `meta['tournament_info']['ranking']` (Sprint 1): `{'metric': 'total_points', 'direction': 'desc', 'tiebreak': ['cooperation_percentage', 'win_rate', 'earliest_submission'], 'shared_rank': False, 'weights': {'points': 1.0, 'cooperation': 0.0, 'win_rate': 0.0}}`
- New meta keys: 1v1 `rounds`, `ranking`, `weights`; N-Player `payoff_model` = `{'type': 'PublicGoodsPayoff', 'name': 'public_goods', 'b': 0.4, 'c': 1, 'nonlinear': {'type': 'linear'}}`; OS `scheduler`.
- Sprint 2 and Final payoffs, weights and settings: "To be released".

**Sprint 1 settings:** 1v1 CC 3,3 · CD 0,5 · DC 5,0 · DD 1,1; all 4 modes, 200 rounds. N-Player Public Goods b=0.4, c=1, groups of 5. OS Round Robin, 8 cores, 100 tasks, homogeneous, 10 runs on the same seeds.
- Itinerary (handoff #1): Sprint 2 1v1 4,4/0,6/6,0/2,2, N-Player b=0.3 groups of 5, OS Priority 8 cores 200 tasks; Final 1v1 4,4/0,7/7,0/2,2, N-Player b=0.25 groups of 8, OS Priority 4 cores 200 tasks (site says "To be released").

**TA announcement (22 Oct ~23:45):** "extra day is now fixed", new tool must be downloaded, "code will be hidden so you cant simply copy other people code and some hidden baseline \ bench marking strategies will be added to the pool to stop you guys from overfitting".

**New app:** releases v1.3.0 (2026-10-22T19:49:44Z), v1.3.1 (2026-10-22T20:19:22Z), **v1.4.0 Latest (2026-10-22T21:03:15Z)**. Latest commits: "Version 1.4.0", "Use several CPU cores for 1v1 and OS runs, same results", "OS simulation: cheaper random draws for memory accesses, same numbers". Not yet downloaded or diffed. FAQ: old app versions are refused by the website.

**Full local tournament, last visible gallery (38 unique entries, seed 1), ranks among students:**
| Game | Us ("yay") | Notes |
|---|---|---|
| OS | **1st, 4.19** | usmicool 4.20, Adaptive Yield 4.21, rayan_sprint1_strategy 4.21, 15 entries 4.23 |
| 1v1 equal weights | 2nd, 71.43 | KT_version 71.52; as_stratv4 66.30 |
| 1v1 points only | **8th, 54.94** | butt_sahab 56.40, Ismile 55.63, fatima_gtft 55.60, sfatima_forgiving3 55.32 (top 20 within about 2.5 points) |
| N-Player equal weights | 6th / 9th / 10th (3 shuffles) | All-cooperating groups draw with score 62.42 (coop 100, points 86.1) vs our group win 52.17 (coop 16) |

**Other measured facts:**
- Look-ahead value (31-entry field, 8 seeds): with peek equal-weights 1st 8/8, points 0.5360; without peek 1st 7/8 (3rd once), points 0.5356; no RNG use at all 0.5321.
- OS study seeds 1-30 (mean avg_response): guide 4.232, recent1 4.206, recent2 4.197, recent3 4.233.
- Engine crash: `run_with_limit` fails with `OverflowError: events set too many times` at call 8,388,607 (2^23 - 1) per process on Python 3.14.4; one OS entry = 301,056 calls (Sprint 1 settings), so about the 28th entry. Bug report drafted, not confirmed sent.
- Hub submit URL limit 7500 characters; current `submit.py` 3436 bytes → 5773-character URL.
- Engine: discounted factor 0.95; stochastic continue 0.995; random mode one length in 100-300; OS `opponents_histories[0][-1]` is the previous signal (current signal is `last_moves[0]`).

## 9. People, terms & names
- **People:** instructor runs the site and tournament; a TA answers questions by text. Classmates known only by entry names.
- **Terms:** "guide's rule" = OS `C` if busy (`last_moves[0]=='D'`) else `D`. "recent1" = guide's rule + also `C` if the previous signal was busy. "Look-ahead"/"peek" = copy `meta['rng']` and read the next draw to find the true last round of a stochastic match. "Express lane" = core 0 (`player_index == 0`) always `C` (usmicool's idea). "Hopeless" (N-Player) = a rival has defected at least as much as us and not cooperated in the last 5 rounds.
- **Names in use:** entry name **yay**; function `sentinel`; app repo `COMPUTATION-NOT-FOUND/ipd-app`; site https://cnf.pythonanywhere.com (pages /announcements, /faq, /results, /tournament, /login).
- **Notable classmate entries:** KT_version (copied our earlier code incl. look-ahead; 1v1 endgame from round 192), waniya_adaptive_v4 (copied our N-Player logic), butt_sahab and Illu_Dellulu_The_4th (fingerprint specific classmates), usmicool (express lane), Adaptive Yield and rayan_sprint1_strategy (OS look back 2), Shahzaib Fareed 30489 (OS checks signal two back).

## 10. Work state
| Item | Status | Version / location | Notes |
|---|---|---|---|
| Live submission | submitted as **yay** | commit `ec58f7b` | OLD (endgame 7). Retuned version below is NOT yet submitted |
| Strategy (commented) | **retuned** (committed 922fe80 = endgame; exploit rule uncommitted until final commit) | `strategies/strategy.py` | Changes vs `ec58f7b`: weight-aware endgame + exploit-non-punishers (`EXPLOIT_PD=0.8`). Tunables at top |
| Submission copy | **regenerated** | `strategies/submit.py` (3561 bytes, URL 6381, safe) | Matches strategy.py (0 mismatches). Resubmit this before 11:59pm with app v1.4.0. Regenerate: `python testing/make_submit.py` |
| Exploit scan | new | `testing/v1_exploit_scan.py` | Per-opponent payoff/coop vs AllD/AllC/TFT/Prober; found `nabiha_strat` as the only pushover |
| Look-ahead version | saved | commit `add7723` | For Sprint 2 if the user wants it |
| Last visible gallery | saved | `local-only/gallery_snapshot_2026-10-22_2337.json` (39 entries) | Code hidden after this |
| New test scripts | in folder, **not committed** | `testing/np_weighted.py`, `testing/v1_sweep.py`, `testing/os_compare.py`, `testing/full/` (common, full_1v1, full_np, full_os) | `np_weighted.py` ranks with equal weights; `load_hub()` defaults to `local-only/strategies.json` (switch to the snapshot if new fetches have no code) |
| Bug report draft | drafted | `bug-report-os-crash.md` | Unknown if sent |
| Private GitHub repo | pushed to `ec58f7b` | https://github.com/fatzzi/ipd-tournament | PRIVATE |
| New app v1.4.0 | not downloaded | Releases page | Needed for submitting and to diff the engine |

## 11. Next steps
1. **DONE (23 Oct):** retuned 1v1 (weight-aware endgame + exploit-non-punishers), crash-proofed with try/except, committed+pushed to origin/main (up to 5075b2b). **Metric correction:** Sprint-1 ranks by `total_points` (not points_percentage my sweeps first used — confirmed in v1.4.0 `ranking.py`). Under the REAL metric our strategy is **[2,3,2,2,2,2,2,1] = 8/8 top-3, mean rank 2.0**, consistent 2nd behind `butt_sahab` (fingerprinter). The exploit rule is decisive (8/8 vs 0/8 without it). Use `testing/v1_metric_check.py`.
2. **DONE: app v1.4.0 engine diff** (downloaded + read-only diffed). Safe on every axis: is_safe_code/extract/PublicGoodsPayoff/OS all identical; our submit passes; we use ≤124 of 200000 line-events. See `sprint1-retune-notes.md` "App v1.4.0 engine diff". **submit.py ready; user resubmits via app v1.4.0 before 11:59pm — validated safe.**
0. **Still open:** download/diff app v1.4.0 engine (below); decide whether to gamble N-Player `D+coop2` (pts% up, rank down — a wash).
2. Ask the user whether to download the new app v1.4.0 source (read-only, own folder) and diff `core_simulation.py`, `n_player_simulation.py`, `app.py` vs `local-only/ipd-app`; re-verify RNG sharing, the 8.4M crash and scoring.
3. If a retune wins clearly, regenerate `submit.py`, check safety + URL length, commit and push, and have the user resubmit before Sprint 1 ends (note: resubmitting moves us later in the tie-break).
4. After Sprint 1 results: read Results, then prepare Sprint 2 (look-ahead from `add7723` if the user still wants it, 1v1 endgame from round 192 to match KT_version, OS rule under the Priority scheduler, all-cooperative N-Player groups).

## 12. Open questions ⚠️
- What exactly ends Sprint 1 on Fri 23 Oct (time of the lock)? Not stated on the site.
- Was the OS crash bug report sent to the instructor/TA? (yes / no)
- Should the look-ahead come back in Sprint 2? User's earlier plan: yes if we don't win Sprint 1 fairly.
- ~~Does the new app (v1.4.0) change the engine?~~ RESOLVED 23 Oct: diffed; safe, OS byte-identical, our submit passes. New: 200k line-event limit (we use ≤124), disqualification for crash/invalid (we crash-proofed).

## 13. Re-attach checklist
- [ ] `handoff-ipd-tournament.md`: this file
- Everything else is on disk in `C:\Users\fxtim\Desktop\ipd-tournament` (open the new chat in that folder). The class token is in `local-only/.env`: [secret removed: re-enter it] only if that file is missing.

---
<sub>Audit: 13/13 sections · 7 rules · 5 corrections · 60 data points · secrets removed: yes · generated by active-memory</sub>
