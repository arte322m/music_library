from typing import Dict, Union, List

import requests
from bs4 import BeautifulSoup


def check(response):
    if response.status_code // 100 != 2:
        raise ConnectionError(f'Неудачный запрос, полученный ответ{response.text}')


def get_info_track(url: str):
    response = requests.get(url, timeout=20)
    check(response)
    result: Dict[Union[str, list]] = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    genres = soup.findAll('a', class_='entAllCats')
    all_genres: List[str] = []
    for genre in genres:
        all_genres.append(genre.text)
    result['genres_tags'] = all_genres
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


def trend_of_main_page(url: str):
    response = requests.get(url, timeout=20)
    check(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    result: Dict[str, Dict[str, Dict[str, Union[str, list]]]] = {}
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


def get_info_track_2(url: str):
    result = {}
    response = requests.get(url, timeout=20)
    check(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    song_details = soup.findAll('div', class_='song_detal_p')
    tags_nav = soup.find('div', class_='path_navigation clearfix')
    tags = tags_nav.findAll('li')
    for tag in tags:
        tag_text = tag.text
        if 'Главная' in tag_text:
            continue
        result.setdefault('genres_tags', [])
        result['genres_tags'].append(tag_text[1:])
    for detail in song_details:
        detail_text = detail.text
        size = detail.find('span', class_='song_zzz').text.split(': ')[1]
        result['size'] = size
        if 'Время' in detail_text:
            duration = detail_text.split(': ')[1]
            result['duration'] = duration.split(' ')[0]
    return result


def top30_week(url: str):
    url = f'{url}top-nedeli/'
    response = requests.get(url, timeout=20)
    check(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = {}
    all_find = soup.findAll('div', class_='song-item')
    for found in all_find:
        track = found.find('span', class_='song_nazv __adv_name').text
        artist = found.find('span', class_='song_artist __adv_artist').text
        url = found.find('a', href=True).get('href')
        result.setdefault(artist, {})
        result[artist].setdefault(track, get_info_track_2(f'https://mp3bob.ru/{url}'))
    return result


FUNCTIONS = {'top30_week': top30_week,
             'trend_of_main_page': trend_of_main_page,
             }


def main():
    pass
    # print(top30_week())
    # trend_of_main_page()


if __name__ == '__main__':
    main()
