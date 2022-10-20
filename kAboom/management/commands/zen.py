from django.core.management.base import BaseCommand
from django.utils import timezone
import os.path
from kAboom.models import Genre


import sqlite3


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('table', type=str, help='Название таблицы')

    def handle(self, *args, **kwargs):
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)
        # print(args)
        # print(kwargs)
        # table = kwargs.get('table')
        # print(table)
        table = kwargs['table']
        if table == 'genre':
            table = 'Genres'
        path = os.path.join(os.getcwd(), 'chinook.db')
        with sqlite3.connect(path) as db:
            cursor = db.cursor()
            cursor_execute = cursor.execute(f"SELECT * FROM {table}")
            db_fetch = cursor_execute.fetchall()
        for genre in db_fetch:
            genre_name = genre[1]
            Genre(name=genre_name).save()
        print(db_fetch)
