import requests

resp = requests.get('https://www.fudan.edu.cn/sitemap.xml', timeout=15)
print(resp.status_code)
print(resp.text[:2000])
