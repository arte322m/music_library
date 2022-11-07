from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import render
from .models import *


def track(request, track_id):
    # track_details = Track.objects.filter(id=track_id)[0]
    track_details = get_object_or_404(Track, id=track_id)
    # genre = get_object_or_404(Genre, id=track_details.genre_id)
    # genre = Genre.objects.filter(id=track_details.genre_id)[0]
    # genre_2 = track_details.genre
    # # media_type = get_object_or_404(MediaType, id=track_details.media_type_id)
    # media_type = MediaType.objects.filter(id=track_details.media_type_id)[0]
    context = {'track_details': track_details}
    return render(request, 'kAboom/track.html', context)


def album(request, album_id):
    # album_info = Album.objects.filter(id=album_id)[0]
    album_info = get_object_or_404(Album, id=album_id)
    track_list = Track.objects.filter(album_id=album_id)
    artist_info = Artist.objects.filter(id=album_info.artist_id)[0]
    artist_info_2 = album_info.artist
    context = {
        'MB': '',
        'artist_info': artist_info,
        'album_info': album_info,
        'track_list': track_list,
    }
    return render(request, 'kAboom/album.html', context)


def artist(request, artist_id):
    # artist_info = Artist.objects.filter(id=artist_id)[0]
    artist_info = get_object_or_404(Artist, id=artist_id)
    album_list = Album.objects.filter(artist_id=artist_id)
    # album_list = get_list_or_404(Album, artist_id=artist_id)

    # album_list_2 = artist_info.album_set.all()

    context = {
        'artist_info': artist_info,
        'album_list': album_list,
    }
    return render(request, 'kAboom/artist.html', context)


def index(request):
    artist_list = Artist.objects.all()
    # artist_list = get_list_or_404(Artist)
    context = {
        'artist_list': artist_list,
    }
    return render(request, 'kAboom/index.html', context)
