import requests
from bs4 import BeautifulSoup

URL_MUZATI = 'https://muzati.net/'
URL_MP3BOB = 'https://mp3bob.ru/load/top-nedeli/'


# class result:
#     pass


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
        result.setdefault('Жанры', [])
        result['Жанры'].append(tag_text[1:])
    for detail in song_details:
        detail_text = detail.text
        size = detail.find('span', class_='song_zzz').text.split(': ')[1]
        result['Размер'] = size
        if 'Время' in detail_text:
            duration = detail_text.split(': ')[1]
            result['Продолжительность'] = duration.split(' ')[0]
    return result


def top30_week():
    response = requests.get(URL_MP3BOB, timeout=20)
    check(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = {}
    all_find = soup.findAll('div', class_='song-item')
    for i in all_find:
        track = i.find('span', class_='song_nazv __adv_name').text
        artist = i.find('span', class_='song_artist __adv_artist').text
        url = i.find('a', href=True).get('href')
        result.setdefault(artist, {})
        result[artist].setdefault(track, get_info_track_2(f'https://mp3bob.ru/{url}'))
    return result


def main():
    print(top30_week())
    # trend_of_main_page()


if __name__ == '__main__':
    main()
