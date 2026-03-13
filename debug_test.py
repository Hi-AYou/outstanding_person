import requests, re
url='http://www.fudan.edu.cn/2019/0426/c427a96253/page.htm'
resp=requests.get(url, timeout=15)
resp.encoding=resp.apparent_encoding
text=resp.text
name='鲍正鹄'
pattern=re.compile(re.escape(name)+r"[\s\S]{0,300}?[\(（]\s*(\d{4})\s*[—\-–]\s*\d{4}\s*[\)）]")
print('match', bool(pattern.search(text)))
if pattern.search(text):
    print(pattern.search(text).group(1))
else:
    m=re.search(r"[\(（]\s*(\d{4})\s*[—\-–]\s*\d{4}\s*[\)）]", text)
    print('fallback', bool(m), m.group(1) if m else '')
