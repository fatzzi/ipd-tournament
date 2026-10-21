# Read-only refresh of the class gallery (same request as the app's "Refresh Gallery").
# Uses local-only/.env for the class website address and token. Never posts anything.
import os, json, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.path.join(HERE, '..', 'local-only')
env = dict(line.strip().split('=', 1) for line in open(os.path.join(LOCAL, '.env')) if '=' in line)
base, token = env['HUB_BASE_URL'].rstrip('/'), env['HUB_API_TOKEN']

for ep in ('strategies', 'practice-strategies'):
    req = urllib.request.Request(f'{base}/api/{ep}', headers={
        'Accept': 'application/json', 'Authorization': f'Bearer {token}'})
    data = json.load(urllib.request.urlopen(req, timeout=20))
    with open(os.path.join(LOCAL, f'{ep}.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1)
    items = data.get('strategies', data) if isinstance(data, dict) else data
    print(f'{ep}: {len(items)}')
    for s in items:
        print('  -', s.get('name'), s.get('type', ''))
