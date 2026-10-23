import sys, json
sys.path.insert(0, r'C:\Users\fxtim\Desktop\ipd-tournament\local-only\ipd-app')
from core_simulation import run_full_simulation
d = json.load(open('local-only/strategies.json', encoding='utf-8')); d = d.get('strategies', d) if isinstance(d, dict) else d
pick = [{'name': s['name'], 'code': s['code']} for s in d if s['name'] in sys.argv[2:]]
pick.append({'name': 'ME', 'code': open('strategies/submit.py').read()})
seed = int(sys.argv[1])
r = run_full_simulation(pick, num_cores=8, seed=seed, scheduler='round_robin', runs=10, num_processes=100)
print(seed, {k: v['avg'].get('avg_response') for k, v in r['strategies'].items()}, r['errors'], flush=True)
