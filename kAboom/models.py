import datetime

from django.db import models
from django.utils import timezone

# var_one_var - переменные и функции и методы классов
# VarOneVar - классы
# varOneVar - Нет
# VAR_ONE_VAR - константы

# null blank default

# Команда для заполнения БД из существующей
# Добавить параметр в команду. Чтобы выбирать какую таблицу заполнять
# python manage.py fill_db --table employees


class MediaType(models.Model):
    name = models.CharField(max_length=120)


class Genre(models.Model):
    name = models.CharField(max_length=120)


class Artist(models.Model):
    name = models.CharField(max_length=120)


class Album(models.Model):
    title = models.CharField(max_length=160)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Track(models.Model):
    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    composer = models.CharField(max_length=220)
    miliseconds = models.IntegerField
    bytes = models.IntegerField
    until_price = models.DecimalField


class Playlist(models.Model):
    track = models.ManyToManyField(Track)
    name = models.CharField(max_length=120)


# class PlaylistTrack(models.Model):
#     # Удалить. Заменить на ManyToMany в треках или плейлисте
#     playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
#     track = models.ForeignKey(Tracks, on_delete=models.CASCADE)


class Employee(models.Model):
    # id = models.
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    # reports_to = models.ForeignKey(, on_delete=models.CASCADE)
    birth_date = models.DateTimeField
    hire_date = models.DateTimeField
    address = models.CharField(max_length=70, default=None)
    city = models.CharField(max_length=40, default=None)
    state = models.CharField(max_length=40, default=None)
    country = models.CharField(max_length=40, default=None)
    postal_code = models.CharField(max_length=10, default=None)
    phone = models.CharField(max_length=24, default=None)
    fax = models.CharField(max_length=24, default=None)
    email = models.CharField(max_length=60, default=None)


class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    company = models.CharField(max_length=80)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    county = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=24)
    fax = models.CharField(max_length=24)
    email = models.CharField(max_length=60)
    support_rep_id = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None)


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inovice_date = models.DateTimeField
    billing_adress = models.CharField
    billing_city = models.CharField


class InvoicesItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    unit_price = models.DecimalField
    quantity = models.IntegerField

