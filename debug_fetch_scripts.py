import requests

base='https://www.fudan.edu.cn'
paths=['/_upload/tpl/00/0e/14/template14/js/list.js','/_upload/tpl/00/0e/14/template14/js/search_az.js']
for path in paths:
    r=requests.get(base+path, timeout=15)
    print(path, r.status_code)
    print(r.text[:2000])
