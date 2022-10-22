from django.core.management.base import BaseCommand
from django.utils import timezone
import os.path
from kAboom.models import *


import sqlite3

# time = timezone.now().strftime('%X')
# self.stdout.write("It's now %s" % time)
# print(args)
# print(kwargs)
# table = kwargs.get('table')
# print(table)
# filter exists

PATH = os.path.join(os.getcwd(), 'chinook.db')


def db_fetch(table):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor_execute = cursor.execute(f"SELECT * FROM {table}")
        return cursor_execute.fetchall()


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('table', type=str, help='Название таблицы')

    def handle(self, *args, **kwargs):
        table = kwargs['table']
        if table == 'genre':
            table = 'genres'
            for genre in db_fetch(table):
                genre_name = genre[1]
                if not Genre.objects.filter(name=genre_name).exists():
                    Genre(name=genre_name).save()
                    pass
                else:
                    print('Поле с таким именем уже есть')

        if table == 'artist':
            table = 'artists'
            for artist in db_fetch(table):
                artist_name = artist[1]
                if not Artist.objects.filter(name=artist_name).exists():
                    Artist(name=artist_name).save()
                else:
                    print('Поле с таким именем уже есть')

        if table == 'mediatype':
            table = 'media_type'
            for media_type in db_fetch(table):
                media_type_name = media_type[1]
                if not MediaType.objects.filter(name=media_type_name).exists():
                    MediaType(name=media_type_name).save()
                else:
                    print('Поле с таким именем уже есть')

        if table == 'playlist':
            table = 'playlists'
            for playlist in db_fetch(table):
                playlist_name = playlist[1]
                if not Playlist.objects.filter(name=playlist_name).exists():
                    Playlist(name=playlist_name).save()
                else:
                    print('Поле с таким именем уже есть')

        if table == 'album':
            table = 'albums'

        if table == 'customer':
            table = 'customers'
        if table == 'employee':
            table = 'employees'
        if table == 'invoice':
            table = 'invoices'
        if table == 'invoiceitem':
            table = 'invoice_items'

        if table == 'track':
            table = 'tracks'
