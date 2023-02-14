from django.db import models
from django.contrib.auth.models import User

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
# МОЙ КАММИТ!!!!!!!


class UserProfile(models.Model):
    DARK = 'DARK'
    LIGHT = 'LIGHT'
    TYPE_OF_THEME = [
        (DARK, 'Dark'),
        (LIGHT, 'Light'),
    ]
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    type_of_theme = models.CharField(max_length=7, choices=TYPE_OF_THEME, default=DARK)


class MediaType(models.Model):

    def __str__(self):
        return self.name
    name = models.CharField(max_length=120)


class GenresTags(models.Model):

    def __str__(self):
        return self.name
    name = models.CharField(max_length=120)


class Artist(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=120)
    favorite = models.ManyToManyField(UserProfile)


class Album(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=160)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(UserProfile)


class Track(models.Model):

    def __str__(self):

        return f'{self.name}, {self.milliseconds//1000//60}:{self.milliseconds//1000%60}:{self.milliseconds%1000}'

    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    genre_tags = models.ManyToManyField(GenresTags)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    composer = models.CharField(max_length=220, null=True)
    milliseconds = models.IntegerField(default=None)
    bytes = models.IntegerField(default=None)
    until_price = models.FloatField(default=None, null=True)
    favorite = models.ManyToManyField(UserProfile)


class Playlist(models.Model):
    track = models.ManyToManyField(Track)
    name = models.CharField(max_length=120)
    favorite = models.ManyToManyField(UserProfile)
    user_maker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Employee(models.Model):
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
