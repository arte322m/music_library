import requests
from bs4 import BeautifulSoup

URL_MUZATI = 'https://muzati.net/'


def check(response):
    if response.status_code // 100 != 2:
        raise ConnectionError(f'Неудачный запрос, полученный ответ{response.text}')


def get_info_track(url: str) -> dict:
    response = requests.get(url, timeout=20)
    check(response)
    result = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    genres = soup.findAll('a', class_='entAllCats')
    all_genres = []
    for genre in genres:
        all_genres.append(genre.text)
    result['genres'] = all_genres
    track_info_all = soup.findAll('div', class_='trackinfo')
    for track_info in track_info_all:
        filtered_track_info = track_info.findAll('li')
        for info in filtered_track_info:
            info_text = info.text
            if 'Продолжительность' in info_text:
                duration = info_text.split(': ')
                result['duration'] = duration[1]
            if 'Размер' in info_text:
                size = info_text.split(': ')
                result['size'] = size[1]
            if 'Формат' in info_text:
                media_format = info_text.split(': ')
                result['format'] = media_format[1]

    return result


def trend_of_main_page():
    response = requests.get(URL_MUZATI, timeout=20)
    check(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = {}
    all_find = soup.findAll('a')
    for found in all_find:
        if found.text == 'Новинки':
            break
        if found.find('div', class_='track-title'):
            artist = found.find('div', class_='track-title').text
            track = found.find('div', class_='song').text
            url = found.get('href')
            result.setdefault(artist, {})
            result[artist].setdefault(track, get_info_track(url))
    return result


def main():
    trend_of_main_page()


if __name__ == '__main__':
    main()
