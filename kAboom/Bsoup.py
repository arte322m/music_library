import requests
from bs4 import BeautifulSoup

URL_MUZATI = 'https://muzati.net/'


def check(url):
    if url.status_code // 100 != 2:
        raise ConnectionError(f'Неудачный запрос, полученный ответ{url.text}')


def get_info_track(url: str) -> list:
    response = requests.get(url, timeout=20)
    check(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = []
    return result


def trend_of_main_page():
    response = requests.get(URL_MUZATI, timeout=20)
    check(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = {}
    all_find = soup.findAll('a')
    for i in all_find:
        if i.text == 'Новинки':
            break
        if i.find('div', class_='track-title'):
            artist = i.find('div', class_='track-title').text
            track = i.find('div', class_='song').text
            url = i.get('href')
            result.setdefault(artist, {})
            result[artist].setdefault(track, get_info_track(url))
    return result


def main():
    print(trend_of_main_page())


if __name__ == '__main__':
    main()
