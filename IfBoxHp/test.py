import re
a=re.compile(r'^[a-zA-Z0-9]+$')
print(a.match("ｊぁ") is None)