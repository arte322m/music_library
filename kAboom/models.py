import datetime, uuid

from django.db import models
from django.utils import timezone

# var_one_var - переменные и функции и методы классов
# VarOneVar - классы
# varOneVar - Нет
# VAR_ONE_VAR - константы


class MediaTypes(models.Model):
    # MediaTypeId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=120)


class Genres(models.Model):
    # GenreId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=120)


class Artists(models.Model):
    # ArtistId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=120)


class Albums(models.Model):
    # album_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=160)
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE)


class Tracks(models.Model):
    # TrackId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    # MediaTypeId = models.ForeignKey(Media_types, on_delete=models.CASCADE)
    media_type = models.ForeignKey(MediaTypes, on_delete=models.CASCADE)
    # media_type_id
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    composer = models.CharField(max_length=220)
    miliseconds = models.IntegerField
    bytes = models.IntegerField
    until_price = models.DecimalField


class Playlists(models.Model):
    # PlaylistId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    track = models.ManyToManyField(Tracks)
    name = models.CharField(max_length=120)


# class PlaylistTrack(models.Model):
#     # Удалить. Заменить на ManyToMany в треках или плейлисте
#     playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
#     track = models.ForeignKey(Tracks, on_delete=models.CASCADE)


class Customers(models.Model):
    # customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
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
    support_rep_id = models.IntegerField


class Invoices(models.Model):
    # InvoiceId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    inovice_date = models.DateTimeField
    billing_adress = models.CharField
    billing_city = models.CharField


class InvoicesItems(models.Model):
    # InvoiceItemId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    unit_price = models.DecimalField
    quantity = models.IntegerField


class Employees(models.Model):
    # employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    reports_to = models.IntegerField
    birth_date = models.DateTimeField
    hire_date = models.DateTimeField
    address = models.CharField
