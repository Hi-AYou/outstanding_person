import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
resp = requests.get('https://www.fudan.edu.cn/427/list.htm', timeout=15, headers=headers)
resp.encoding = resp.apparent_encoding
text = resp.text

for name in ['钟学礼','鲍正鹄','蔡尚思','陈传璋','陈望道']:
    print(name, name in text)
print('html length', len(text))
print('c427 count', text.count('c427'))

