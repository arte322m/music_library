from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from django.core.paginator import Paginator


def genre(request, genre_id):
    genre_info = get_object_or_404(Genre, id=genre_id)
    context = {
        'genre_info': genre_info,
    }
    return render(request, 'kAboom/genre.html', context)


def genres(request):
    genre_list = Genre.objects.all()
    context = {
        'genre_list': genre_list,
    }
    return render(request, 'kAboom/genres.html', context)


def track(request, track_id):
    track_details = get_object_or_404(Track, id=track_id)
    album_info = track_details.album
    artist_info = album_info.artist
    context = {
        'track_details': track_details,
        'artist_info': artist_info,
    }
    return render(request, 'kAboom/track.html', context)


def album(request, album_id):
    # album_info = Album.objects.filter(id=album_id)[0]
    album_info = get_object_or_404(Album, id=album_id)
    track_list = Track.objects.filter(album_id=album_id)
    artist_info = Artist.objects.filter(id=album_info.artist_id)[0]
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
    paginator = Paginator(artist_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'kAboom/index.html', context)
