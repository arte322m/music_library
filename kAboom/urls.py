from django.urls import path

from . import views

app_name = 'kAboom'
urlpatterns = [
    path('', views.index, name='index'),
    path('genre/', views.genres, name='genres'),
    path('genre/<int:genre_id>', views.genre, name='genre'),
    path('artist/<int:artist_id>/', views.artist, name='artist'),
    path('album/<int:album_id>/', views.album, name='album'),
    path('track/<int:track_id>/', views.track, name='track'),
]
