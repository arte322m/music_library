from django.shortcuts import render, get_object_or_404
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect


def track(request, album_id):
    track_list = Track.objects.filter(album_id=album_id)
    context = {
        'track_list': track_list,
    }
    return render(request, 'kAboom/track.html', context)


def album(request, artist_id):
    album_list = Album.objects.filter(artist_id=artist_id)
    context = {
        'album_list': album_list,
    }
    return render(request, 'kAboom/album.html', context)


def index(request):
    artist_list = Artist.objects.all()
    context = {
        'artist_list': artist_list,
    }
    return render(request, 'kAboom/index.html', context)
