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
# Переписать на орм.Objects

PATH = os.path.join(os.getcwd(), 'chinook.db')
PATH_DB_NEW = os.path.join(os.getcwd(), 'db.sqlite3')


def db_fetch(table, path):
    with sqlite3.connect(path) as db:
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
            for genre in db_fetch(table, PATH):
                genre_name = genre[1]
                if Genre.objects.filter(name=genre_name).exists():
                    print('Поле с таким именем уже есть')
                else:
                    Genre(name=genre_name).save()
            print('complete')

        if table == 'artist':
            table = 'artists'
            for artist in db_fetch(table, PATH):
                artist_name = artist[1]
                if Artist.objects.filter(name=artist_name).exists():
                    print('Поле с таким именем уже есть')
                else:
                    Artist(name=artist_name).save()
            print('complete')

        if table == 'mediatype':
            table = 'media_types'
            for media_type in db_fetch(table, PATH):
                media_type_name = media_type[1]
                if MediaType.objects.filter(name=media_type_name).exists():
                    print('Поле с таким именем уже есть')
                else:
                    MediaType(name=media_type_name).save()
            print('complete')

        if table == 'playlist':
            table = 'playlists'
            for playlist in db_fetch(table, PATH):
                playlist_name = playlist[1]
                Playlist(name=playlist_name).save()
            print('complete')

        if table == 'album':
            table = 'albums'

            artist_name_id = {}
            artist_table = Artist.objects.all()
            for artist in artist_table:
                artist_name_id[artist.name] = artist.id

            artist_id_name_foreign = {}
            for artist in db_fetch('artists', PATH):
                artist_id_name_foreign[artist[0]] = artist[1]

            for album in db_fetch(table, PATH):
                album_title = album[1]

                artist_id = album[2]
                artist_name = artist_id_name_foreign[artist_id]
                artist_id_true = artist_name_id[artist_name]

                if Album.objects.filter(title=album_title, artist_id=artist_id_true).exists():
                    print('Поле с таким именем уже есть')
                else:
                    Album(title=album_title, artist_id=artist_id).save()
            print('complete')

        if table == 'track':
            table = 'tracks'

            album_name_id = {}
            album_table = Album.objects.all()
            for album in album_table:
                album_name_id[album.title] = album.id

            album_id_name_foreign = {}
            for album in db_fetch('albums', PATH):
                album_id_name_foreign[album[0]] = album[1]

            genre_name_id = {}
            genre_table = Genre.objects.all()
            for genre in genre_table:
                genre_name_id[genre.name] = genre.id

            genre_id_name_foreign = {}
            for genre in db_fetch('genres', PATH):
                genre_id_name_foreign[genre[0]] = genre[1]

            media_type_name_id = {}
            media_type_table = MediaType.objects.all()
            for media_type in media_type_table:
                media_type_name_id[media_type.name] = media_type.id
            media_type_id_name_foreign = {}
            for media_type in db_fetch('media_types', PATH):
                media_type_id_name_foreign[media_type[0]] = media_type[1]

            for track in db_fetch(table, PATH):
                track_name = track[1]
                track_composer = track[5]

                album_id = track[2]
                album_name = album_id_name_foreign[album_id]
                album_id_true = album_name_id[album_name]

                genre_id = track[4]
                genre_name = genre_id_name_foreign[genre_id]
                genre_id_true = genre_name_id[genre_name]

                media_type_id = track[3]
                media_type_name = media_type_id_name_foreign[media_type_id]
                media_type_id_true = media_type_name_id[media_type_name]

                milliseconds = track[6]
                bytes = track[7]
                until_price = track[8]
                if not Track.objects.filter(
                        name=track_name,
                        composer=track_composer,
                        album_id=album_id,
                        milliseconds=milliseconds).exists():
                    Track(
                        name=track_name,
                        composer=track_composer,
                        album_id=album_id_true,
                        genre_id=genre_id_true,
                        media_type_id=media_type_id_true,
                        milliseconds=milliseconds,
                        bytes=bytes,
                        until_price=until_price
                    ).save()
                else:
                    print('Поле с таким именем уже есть')
            print('complete')

        if table == 'employee':
            table = 'employees'
            for employee in db_fetch(table, PATH):
                last_name = employee[1]
                first_name = employee[2]
                title = employee[3]
                reports_to_id = employee[4]
                birth_date = employee[5]
                hire_date = employee[6]
                address = employee[7]
                city = employee[8]
                state = employee[9]
                country = employee[10]
                postal_code = employee[11]
                phone = employee[12]
                fax = employee[13]
                email = employee[14]
                if not Employee.objects.filter(last_name=last_name, first_name=first_name, phone=phone).exists():
                    Employee(
                        last_name=last_name,
                        first_name=first_name,
                        title=title,
                        reports_to_id=reports_to_id,
                        birth_date=birth_date,
                        hire_date=hire_date,
                        address=address,
                        city=city,
                        state=state,
                        country=country,
                        postal_code=postal_code,
                        phone=phone,
                        fax=fax,
                        email=email
                    ).save()
                else:
                    print('Поле с таким именем уже есть')
            print('complete')

        if table == 'customer':
            table = 'customers'

            for customer in db_fetch(table, PATH):
                first_name = customer[1]
                last_name = customer[2]
                company = customer[3]
                address = customer[4]
                city = customer[5]
                state = customer[6]
                country = customer[7]
                postal_code = customer[8]
                phone = customer[9]
                fax = customer[10]
                email = customer[11]
                support_rep_id = customer[12]

                if not Customer.objects.filter(first_name=first_name, last_name=last_name, phone=phone).exists():
                    Customer(
                        first_name=first_name,
                        last_name=last_name,
                        company=company,
                        address=address,
                        city=city,
                        state=state,
                        country=country,
                        postal_code=postal_code,
                        phone=phone,
                        fax=fax,
                        email=email,
                        support_rep_id=support_rep_id
                    ).save()
                else:
                    print('Поле с таким именем уже есть')
            print('complete')

        if table == 'invoice':
            table = 'invoices'

            for invoice in db_fetch(table, PATH):
                customer_id = invoice[1]
                invoice_date = invoice[2]
                billing_address = invoice[3]
                billing_city = invoice[4]
                billing_state = invoice[5]
                billing_country = invoice[6]
                billing_postal_code = invoice[7]
                total = invoice[8]
                if Invoice.objects.filter(customer_id=customer_id, invoice_date=invoice_date, total=total).exists():
                    print('Поле с таким именем уже есть')
                else:
                    Invoice(
                        customer_id=customer_id,
                        invoice_date=invoice_date,
                        billing_address=billing_address,
                        billing_city=billing_city,
                        billing_state=billing_state,
                        billing_country=billing_country,
                        billing_postal_code=billing_postal_code,
                        total=total
                    ).save()
            print('complete')

        if table == 'invoiceitem':
            table = 'invoice_items'

            for invoices_item in db_fetch(table, PATH):
                invoice_id = invoices_item[1]
                track_id = invoices_item[2]
                unit_price = invoices_item[3]
                quantity = invoices_item[4]
                if InvoicesItem.objects.filter(invoice_id=invoice_id, track_id=track_id).exists():
                    print('Поле с таким именем уже есть')
                else:
                    InvoicesItem(
                        invoice_id=invoice_id,
                        track_id=track_id,
                        unit_price=unit_price,
                        quantity=quantity,
                    ).save()
            print('complete')

        if table == 'playlisttrack':
            table = 'playlist_track'

            for playlist_track in db_fetch(table, PATH):
                playlist_id = playlist_track[0]
                track_id = playlist_track[1]
                a = Playlist.objects.filter(id=playlist_id)[0]
                b = Track.objects.filter(id=track_id)[0]
                a.track.add(b)
