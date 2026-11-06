import json, base64, sys, os
# usage: extract.py <tool-result-json> <outdir>
p, out = sys.argv[1], sys.argv[2]
data = json.load(open(p))
txt = data[0]['text'] if isinstance(data, list) else data
obj = json.loads(txt)
name = obj['title']
open(os.path.join(out, name), 'wb').write(base64.b64decode(obj['content']))
print(name, len(base64.b64decode(obj['content'])))
