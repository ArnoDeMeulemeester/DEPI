import requests

url = 'http://www.facebook.com'
res = requests.get(url)

txt = res.text
status = res.status_code

print(txt, status)