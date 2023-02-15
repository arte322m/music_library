from django.urls import path
from . import views


app_name = 'kAboom'
urlpatterns = [
    path('', views.main, name='main'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/registration/', views.registration, name='registration'),
    path('favorites/<int:user_id>', views.favorites, name='favorites'),
    path('favorite_track/', views.favorite_track, name='favorite_track'),
    path('favorite_playlist/', views.favorite_playlist, name='favorite_playlist'),
    path('my_playlists/', views.my_playlists, name='my_playlists'),
    path('favorite_album/', views.favorite_album, name='favorite_album'),
    path('favorite_artist/', views.favorite_artist, name='favorite_artist'),
    path('track_search/', views.track_search, name='track_search'),
    path('search/<str:search_text>', views.search, name='search'),
    path('playlist_creation/', views.playlist_creation, name='playlist_creation'),
    path('playlist/change_playlist/<int:playlist_id>', views.change_playlist, name='change_playlist'),
    path('playlist/change_playlist', views.change_playlist_view, name='change_playlist_view'),
    path('playlist_delete/', views.playlist_delete, name='playlist_delete'),
    path('artist/', views.artist_index, name='artist_index'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('genre/', views.genre_index, name='genre_index'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),
    path('track/', views.track_index, name='track_index'),
    path('track/<int:track_id>/', views.track_detail, name='track_detail'),
    path('album/', views.album_index, name='album_index'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('playlist/', views.playlist_index, name='playlist_index'),
    path('playlist/<int:playlist_id>', views.playlist_detail, name='playlist_detail'),
    path('switch_theme/', views.switch_theme, name='switch_theme'),
    path('muzati_trend/<str:name>', views.muzati_trend, name='muzati_trend'),
    path('add_track/', views.add_track, name='add_track'),
    path('parser/', views.parser, name='parser'),
]
