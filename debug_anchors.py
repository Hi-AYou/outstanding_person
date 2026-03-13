import requests
from bs4 import BeautifulSoup

resp = requests.get('https://www.fudan.edu.cn/427/list.htm', timeout=15)
resp.encoding = resp.apparent_encoding
soup = BeautifulSoup(resp.text, 'html.parser')

found = []
for a in soup.find_all('a', href=True):
    h = a['href']
    if 'c427' in h or '/427/' in h or 'page.htm' in h:
        found.append((a.get_text().strip(), h))

for t, h in found[:200]:
    print(repr(t), h)

print('--- total', len(found))
print('\nScripts:')
for s in soup.find_all('script'):
    if s.get('src'):
        print(s.get('src'))
    else:
        txt = s.string
        if txt and 'ajax' in txt:
            print('inline script with ajax')
