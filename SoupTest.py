#Testscenario van de tutorial

import requests
import urllib.request
from bs4 import BeautifulSoup

#url site
url = 'http://web.mta.info/developers/turnstile.html'

#Connect to URL
response = requests.get(url)
print(response)

#Parsen van HTML en oplsaan in BS4-bject
obj = BeautifulSoup(response.text, "html.parser")
print(obj)

#localiseer gezochte html-tag (hier link met download)
obj.findAll('a')

#bekijken hoe de downloadlink werkt en aanpassen waar nodig
link = obj.findAll('a')[36]['href']
print(link)

#automatisch downloaden van file na link gevonden te hebben
#download_url = 'http://web.mta.info/developers/' + link
#urllib.request.urlretrieve(download_url)