import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/Earth'

r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
soup.prettify()
find = soup.find('table', class_='infobox')



final = find.find_all('tr')

for a, i in enumerate(final):
    box = i.find('th')
    try:
        divi = box.find('div')
    except AttributeError:
        continue

    try:
        finfin = divi.find('a', title = 'Orbital period')
        if finfin != None:
            res = i.find('td')
            resres = res.find('span')
            print(resres.get_text())
    except AttributeError:
        continue
    
