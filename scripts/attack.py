"""Simula fuerza bruta de login para generar un incidente visible en Grafana."""
import http.cookiejar, re, sys, time, urllib.error, urllib.parse, urllib.request
base = sys.argv[1] if len(sys.argv) > 1 else "http://securedev-app:8000"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
html = op.open(base + "/login").read().decode()
m = re.search(r'name="csrf_token" value="([^"]+)"', html)
for i in range(n):
    data = {"username": "ana", "password": f"incorrecta{i}"}
    if m: data["csrf_token"] = m.group(1)
    try:
        r = op.open(base + "/login", urllib.parse.urlencode(data).encode()); code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    print(i + 1, code); time.sleep(0.3)
