import json
d = {}
d['python'] = {"compiler":"bin/addHeader.py"}
a = json.dumps(d)
f = open("language.json","w")
f.write(a)
