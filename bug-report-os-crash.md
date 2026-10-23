**Subject:** Possible engine bug: "events set too many times" after many strategy calls (Python 3.12+)

Hi,

While testing locally with the class app, I ran into an engine error that might affect the tournament runs, especially the OS simulation.

**What happens**
After a certain number of strategy calls in one Python process, every later call fails with:

```
OverflowError: events set too many times
```

The strategy that is running at that point, and every strategy after it, is reported as failing, even though their code is fine. Entries are evaluated in list order, so the ones near the end of the list are the ones affected.

**Minimal reproduction** (from the app folder, Python 3.14.4 on Windows):

```python
from n_player_simulation import run_with_limit
f = lambda: 'C'
i = 0
while True:
    run_with_limit(f)
    i += 1
```

It fails at call 8,388,607 (2^23 - 1).

**Likely cause**
`run_with_limit` calls `sys.settrace(...)` and `sys.settrace(None)` around every strategy call. From Python 3.12, `settrace` runs on top of the new `sys.monitoring` machinery, which keeps a per-process version counter. Each call increments that counter, and it overflows after about 8.4 million calls. The OS simulation makes one strategy call per dispatch per core per run, so with a large field, one process can reach that count during a single tournament.

**Possible fixes**
- Run the tournament on Python 3.11, where `settrace` doesn't use this counter, or
- Set the trace function once per strategy, workload or run rather than once per call (or count instructions in a different way), or
- Evaluate each strategy in a fresh process.

I haven't checked which Python version the class site uses, so this may not affect the official runs. I wanted to flag it in case it does.

Thanks,
Fatima
