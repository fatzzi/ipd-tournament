from common import *
from core_simulation import run_full_simulation
name = sys.argv[1]
d = json.load(open(GAL, encoding='utf-8')); d = d.get('strategies', d) if isinstance(d, dict) else d
code = next(s['code'] for s in d if s['name'] == name)
r = run_full_simulation([{'name': name, 'code': code}], num_cores=8, seed=1, scheduler='round_robin', runs=10, num_processes=100)
v = r['strategies'].get(name, {}).get('avg', {}).get('avg_response')
print(json.dumps({'name': name, 'avg_response': v, 'errors': [e['reason'] for e in r['errors']]}), flush=True)
