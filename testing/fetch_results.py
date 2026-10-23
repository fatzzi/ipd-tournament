# Read-only fetch of the class website's published results (GET only, never posts).
# Saves raw pages under local-only/results/ (gitignored). Uses local-only/.env for the address/token.
import os, re, json, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.path.join(HERE, '..', 'local-only')
OUT = os.path.join(LOCAL, 'results')
os.makedirs(OUT, exist_ok=True)
env = dict(line.strip().split('=', 1) for line in open(os.path.join(LOCAL, '.env')) if '=' in line)
base, token = env['HUB_BASE_URL'].rstrip('/'), env['HUB_API_TOKEN']
HDR = {'Authorization': f'Bearer {token}', 'X-IPD-App-Version': '1.4.0', 'User-Agent': 'ipd-results-reader'}


def get(path, accept='text/html'):
    req = urllib.request.Request(base + path, headers={**HDR, 'Accept': accept})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')


def save(name, text):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(text)


st, html = get('/results')
save('results_index.html', html)
print('/results ->', st, len(html), 'bytes')
# Every in-site link that looks like a result / json endpoint.
links = sorted(set(re.findall(r'''href=["'](/[^"'#?]*(?:result|api)[^"'#]*)["']''', html)))
print('result-ish links:', links)
for p in links:
    s, body = get(p, 'application/json, text/html')
    fname = re.sub(r'[^A-Za-z0-9]+', '_', p.strip('/')) + ('.json' if body.lstrip().startswith(('{', '[')) else '.html')
    save(fname, body)
    print(f'  {p} -> {s} {len(body)} bytes -> {fname}')
for p in ('/api/results', '/api/snapshots', '/announcements', '/faq', '/tournament'):
    s, body = get(p, 'application/json, text/html')
    fname = re.sub(r'[^A-Za-z0-9]+', '_', p.strip('/')) + ('.json' if body.lstrip().startswith(('{', '[')) else '.html')
    save(fname, body)
    print(f'{p} -> {s} {len(body)} bytes -> {fname}')
