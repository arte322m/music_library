from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from django.core.paginator import Paginator


def main(request):
    return render(request, 'kAboom/main.html')


def artist_index(request):
    artist_list = Artist.objects.all()
    paginator = Paginator(artist_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'kAboom/artist_index.html', context)


def artist_detail(request, artist_id):
    artist_info = get_object_or_404(Artist, id=artist_id)
    album_list = Album.objects.filter(artist_id=artist_id)

    context = {
        'artist_info': artist_info,
        'album_list': album_list,
    }
    return render(request, 'kAboom/artist_detail.html', context)


def genre_index(request):
    genre_list = Genre.objects.all()
    context = {
        'genre_list': genre_list,
    }
    return render(request, 'kAboom/genre_index.html', context)


def genre_detail(request, genre_id):
    genre_info = get_object_or_404(Genre, id=genre_id)
    context = {
        'genre_info': genre_info,
    }
    return render(request, 'kAboom/genre_detail.html', context)


def track_index(request):
    track_list = Track.objects.all()
    paginator = Paginator(track_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'kAboom/track_index.html', context)


def track_detail(request, track_id):
    track_details = get_object_or_404(Track, id=track_id)
    album_info = track_details.album
    artist_info = album_info.artist
    context = {
        'track_details': track_details,
        'artist_info': artist_info,
    }
    return render(request, 'kAboom/track_detail.html', context)


def album_index(request):
    album_list = Album.objects.all()
    paginator = Paginator(album_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'kAboom/album_index.html', context)


def album_detail(request, album_id):
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
    return render(request, 'kAboom/album_detail.html', context)


def playlist_index(request):
    playlist_list = Playlist.objects.all()
    paginator = Paginator(playlist_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'playlist_list': playlist_list,
    }
    return render(request, 'kAboom/playlist_index.html', context=context)


def playlist_detail(request, playlist_id):
    playlist_info = get_object_or_404(Playlist, id=playlist_id)
    track_list = Playlist.objects.get(id=playlist_id).track.all()
    paginator = Paginator(track_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'playlist_info': playlist_info,
        'track_list': track_list,
    }
    return render(request, 'kAboom/playlist_detail.html', context=context)
