from django.contrib import admin
from .models import MediaType, GenresTags, Artist, Album, Track, Playlist, Customer, Invoice, InvoicesItem, Employee,\
    Parser

admin.site.register(MediaType)
admin.site.register(GenresTags)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(InvoicesItem)
admin.site.register(Employee)
admin.site.register(Parser)
