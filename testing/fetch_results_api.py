# Read-only: pull every published result (1v1, N-Player, OS) + the frozen submission snapshot
# from the class website's JSON API into local-only/results/ (gitignored). GET only.
import os, json, urllib.request, urllib.error
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.path.join(HERE, '..', 'local-only')
OUT = os.path.join(LOCAL, 'results')
os.makedirs(OUT, exist_ok=True)
env = dict(line.strip().split('=', 1) for line in open(os.path.join(LOCAL, '.env')) if '=' in line)
base, token = env['HUB_BASE_URL'].rstrip('/'), env['HUB_API_TOKEN']
HDR = {'Authorization': f'Bearer {token}', 'X-IPD-App-Version': '1.4.0', 'Accept': 'application/json'}


def get(path):
    req = urllib.request.Request(base + path, headers=HDR)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, {'error': e.read().decode('utf-8', 'replace')[:300]}


def dump(name, obj):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=1)


def items(d, *keys):
    if isinstance(d, list):
        return d
    for k in keys:
        if isinstance(d, dict) and isinstance(d.get(k), list):
            return d[k]
    return []


for kind, lst, detail in (('1v1', '/api/tournaments', '/api/tournament/'),
                          ('nplayer', '/api/nplayer/tournaments', '/api/nplayer/tournament/'),
                          ('os', '/api/os-simulations', '/api/os-simulation/')):
    st, data = get(lst)
    dump(f'{kind}_list.json', data)
    rows = items(data, 'tournaments', 'simulations', 'results', 'items')
    print(f'{lst} -> {st}, {len(rows)} entries')
    for t in rows:
        tid = t.get('id') or t.get('_id')
        print(f'   id={tid} name={t.get("name")!r} date={t.get("created_at") or t.get("date") or t.get("timestamp")}')
        if tid:
            s, d = get(detail + quote(str(tid), safe=''))
            dump(f'{kind}_{tid}.json', d)
            print(f'      detail -> {s}, keys={list(d)[:12] if isinstance(d, dict) else type(d).__name__}')

for p in ('/api/tournament/schedule', '/api/nplayer/schedule', '/api/os-simulation/schedule'):
    s, d = get(p)
    dump(p.strip('/').replace('/', '_') + '.json', d)
    print(f'{p} -> {s}: {json.dumps(d)[:300]}')

st, snaps = get('/api/snapshots')
for sn in items(snaps, 'snapshots'):
    s, d = get(f'/api/snapshots/{quote(sn["id"], safe="")}/strategies')
    dump(f'snapshot_{sn["id"]}.json', d)
    strats = d.get('strategies', []) if isinstance(d, dict) else []
    with_code = sum(1 for x in strats if (x.get('code') or '').strip())
    print(f'snapshot {sn["label"]} -> {s}: {len(strats)} strategies, {with_code} with code')
