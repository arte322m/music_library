import requests
from bs4 import BeautifulSoup

URL_MUZATI = 'https://muzati.net/'


def check(url):
    if url.status_code // 100 != 2:
        raise ConnectionError(f'Неудачный запрос, полученный ответ{url.text}')


def get_info_track(url: str) -> dict:
    response = requests.get(url, timeout=20)
    check(response)
    result = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    genres = soup.findAll('a', class_='entAllCats')
    all_genres = []
    for i in genres:
        all_genres.append(i.text)
    result['Жанры'] = all_genres
    track_info_all = soup.findAll('div', class_='trackinfo')
    for i in track_info_all:
        track_info = i.findAll('li')
        duration = track_info[1].text
        size = track_info[2].text
        format = track_info[5].text
        result['Продолжительность'] = duration
        result['Размер'] = size
        result['Формат'] = format

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
