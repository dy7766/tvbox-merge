import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://cdn.jsdelivr.net/gh/dy7766/tvbox-merge@main/merged.json',
    'https://fastly.jsdelivr.net/gh/dy7766/tvbox-merge@main/merged.json',
    'https://gcore.jsdelivr.net/gh/dy7766/tvbox-merge@main/merged.json',
    'https://testingcf.jsdelivr.net/gh/dy7766/tvbox-merge@main/merged.json',
    'https://raw.gitmirror.com/dy7766/tvbox-merge/main/merged.json',
    'https://ghp.ci/https://raw.githubusercontent.com/dy7766/tvbox-merge/main/merged.json',
    'https://ghproxy.net/https://raw.githubusercontent.com/dy7766/tvbox-merge/main/merged.json',
    'https://mirror.ghproxy.com/https://raw.githubusercontent.com/dy7766/tvbox-merge/main/merged.json',
    'https://raw.githubusercontent.com/dy7766/tvbox-merge/main/merged.json',
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'okhttp/3.15.0'})
    try:
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            data = resp.read()
            print(f"{resp.status} (len={len(data)}): {u}")
    except Exception as e:
        print(f"FAILED ({e}): {u}")
