import urllib.request
import re

url = 'https://cdn.jsdelivr.net/gh/gaotianliuyun/gao@master/lib/drpy2.min.js'
content = urllib.request.urlopen(url).read().decode('utf-8')
print("Len:", len(content))
for match in re.finditer(r'([a-zA-Z0-9_\.]+\.(?:js|json|jar|txt))', content):
    print("Ref:", match.group(1))
