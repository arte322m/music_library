import datetime

from django.db import models
from django.utils import timezone

# var_one_var - переменные и функции и методы классов
# VarOneVar - классы
# varOneVar - Нет
# VAR_ONE_VAR - константы
# null blank default
# список artist/album/track
# Команда для заполнения БД из существующей
# Добавить параметр в команду. Чтобы выбирать какую таблицу заполнять
# python manage.py fill_db --table employees
# class Playlists.ForeignKey(Tracks, on_delete=models.CASCADE)


class MediaType(models.Model):
    name = models.CharField(max_length=120)


class Genre(models.Model):
    name = models.CharField(max_length=120)


class Artist(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=120)


class Album(models.Model):
    title = models.CharField(max_length=160)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Track(models.Model):

    def __str__(self):
        return f'{self.name}, {self.milliseconds}'

    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    composer = models.CharField(max_length=220, null=True)
    milliseconds = models.IntegerField(default=None)
    bytes = models.IntegerField(default=None)
    until_price = models.FloatField(default=None)


class Playlist(models.Model):
    track = models.ManyToManyField(Track)
    name = models.CharField(max_length=120)


class Employee(models.Model):
    # id = models.
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    reports_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    birth_date = models.DateTimeField(null=True)
    hire_date = models.DateTimeField(null=True)
    address = models.CharField(max_length=70, default=None)
    city = models.CharField(max_length=40, default=None)
    state = models.CharField(max_length=40, default=None)
    country = models.CharField(max_length=40, default=None)
    postal_code = models.CharField(max_length=10, default=None)
    phone = models.CharField(max_length=24, default=None)
    fax = models.CharField(max_length=24, default=None)
    email = models.EmailField(max_length=60, default=None)


class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    company = models.CharField(max_length=80, null=True)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40, null=True)
    country = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=24, null=True)
    fax = models.CharField(max_length=24, null=True)
    email = models.EmailField(max_length=60)
    support_rep = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(null=True)
    billing_address = models.CharField(max_length=70, null=True)
    billing_city = models.CharField(max_length=40, null=True)
    billing_state = models.CharField(max_length=40, null=True)
    billing_country = models.CharField(max_length=40, null=True)
    billing_postal_code = models.CharField(max_length=40, null=True)
    total = models.FloatField(default=None)


class InvoicesItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    unit_price = models.IntegerField(default=None)
    quantity = models.IntegerField(default=None)
