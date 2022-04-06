import requests
import bs4

res = requests.get('https://google.com/search?q=' + 'arvid')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")
print(soup.prettify())
links = soup.select('.r a')
print(links)