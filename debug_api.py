import requests, json
headers={'User-Agent':'Mozilla/5.0'}
url='https://www.fudan.edu.cn/_wp3services/generalQuery?queryObj=articles&siteId=2&columnId=427&rows=200'
resp = requests.get(url, headers=headers, timeout=15)
print('status', resp.status_code)
try:
    j = resp.json()
    print('keys', list(j.keys())[:20])
    print(json.dumps(j, ensure_ascii=False)[:4000])
except Exception:
    print('text len', len(resp.text))
    print(resp.text[:2000])
