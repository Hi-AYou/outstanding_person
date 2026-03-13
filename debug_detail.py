import requests
url='http://www.fudan.edu.cn/2019/0426/c427a96253/page.htm'
resp=requests.get(url, timeout=15)
resp.encoding=resp.apparent_encoding
print(resp.text[:2000])
