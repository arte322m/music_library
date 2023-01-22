import requests
from bs4 import BeautifulSoup

response = requests.get('https://muzati.net/', timeout=20).text
soup = BeautifulSoup(response, 'html.parser')

filtered = {}
all_find = soup.findAll('a')
for i in all_find:
    if i.text == 'Новинки':
        break
    if i.find('div', class_='track-title'):
        filtered[i.find('div', class_='track-title').text] = [
            i.find('div', class_='song').text,
            i.find('div', class_='songinfo').text,
            i.get('href')
        ]

for i in filtered.items():
    print(i)
