from typing import Callable

from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .parsers import trend_of_main_page, top30_week, FUNCTIONS
from .models import UserProfile, Album, Playlist, Artist, Track, GenreTag, MediaType, Parser


@login_required
@require_POST
def favorite_album(request):
    user_info = UserProfile.objects.get(user_id=request.user.id)
    album_details = Album.objects.get(id=request.POST['album_id'])

    if request.POST['fav'] == 'rem':
        album_details.favorite.remove(user_info)
    elif request.POST['fav'] == 'add':
        album_details.favorite.add(user_info)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def favorite_playlist(request):
    user_info = UserProfile.objects.get(user_id=request.user.id)
    playlist_details = Playlist.objects.get(id=request.POST['playlist_id'])

    if request.POST['fav'] == 'rem':
        playlist_details.favorite.remove(user_info)
    elif request.POST['fav'] == 'add':
        playlist_details.favorite.add(user_info)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def favorite_artist(request):
    user_info = UserProfile.objects.get(user_id=request.user.id)
    artist_details = Artist.objects.get(id=request.POST['artist_id'])

    if request.POST['fav'] == 'rem':
        artist_details.favorite.remove(user_info)
    elif request.POST['fav'] == 'add':
        artist_details.favorite.add(user_info)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def favorite_track(request):
    user_info = UserProfile.objects.get(user_id=request.user.id)
    track_details = Track.objects.get(id=request.POST['track_id'])

    if request.POST['fav'] == 'rem':
        track_details.favorite.remove(user_info)
    elif request.POST['fav'] == 'add':
        track_details.favorite.add(user_info)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def favorites(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    tracks = user_profile.track_set.all()
    playlists = user_profile.playlist_set.all()
    artists = user_profile.artist_set.all()
    albums = user_profile.album_set.all()
    context = {
        'tracks': tracks,
        'artists': artists,
        'albums': albums,
        'playlists': playlists,
    }
    return render(request, 'kAboom/favorites.html', context)


def registration(request):
    if request.method == 'POST':
        username = request.POST['login']
        if User.objects.filter(username=username):
            return render(request, 'kAboom/registration.html', {'error_message': 'Имя пользователя занято'})
        if request.POST['password'] != request.POST['repeat_password']:
            return render(request, 'kAboom/registration.html', {'error_message': 'Пароли не совпадают'})
        user = User.objects.create_user(username=username, password=request.POST['password'])
        UserProfile(user_id=user.id).save()
        login(request, user)
        return redirect(reverse('kAboom:main'))
    return render(request, 'kAboom/registration.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            profile_id = User.objects.get(username=username).id
            profile = UserProfile.objects.filter(user_id=profile_id)
            if not profile:
                UserProfile(user_id=profile_id).save()
            if UserProfile.objects.get(user_id=profile_id).type_of_theme == UserProfile.DARK:
                request.session['theme'] = UserProfile.DARK
            else:
                request.session['theme'] = UserProfile.LIGHT
            return redirect(reverse('kAboom:main'))
        if not User.objects.filter(username=username):
            return render(request, 'kAboom/login.html', {'error_message': 'Такого логина не существует'})
        return render(request, 'kAboom/login.html', {'error_message': 'Неправильный пароль'})
    return render(request, 'kAboom/login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('kAboom:main'))


def main(request):
    track_rating = Track.objects.prefetch_related('favorite').annotate(
        num_favorite_tracks=Count('favorite')).order_by('-num_favorite_tracks')[:10]
    context = {
        'track_rating': track_rating
    }

    return render(request, 'kAboom/main.html', context)


def artist_index(request):
    artist_list = Artist.objects.all()
    paginator = Paginator(artist_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(user_id=request.user.id)
        favorite_artists = user_info.artist_set.all()
        context['favorite_artists'] = favorite_artists

    return render(request, 'kAboom/artist_index.html', context)


def artist_detail(request, artist_id):
    artist_info = get_object_or_404(Artist, id=artist_id)
    album_list = Album.objects.filter(artist_id=artist_id)

    context = {
        'artist_info': artist_info,
        'album_list': album_list,
    }

    if request.user.is_authenticated:
        artist_is_favorite = artist_info.favorite.filter(user=request.user).exists()

        context['artist_is_favorite'] = artist_is_favorite

    return render(request, 'kAboom/artist_detail.html', context)


def genre_index(request):
    genre_list = GenreTag.objects.all().order_by('name')
    context = {
        'genre_list': genre_list,
    }
    return render(request, 'kAboom/genre_index.html', context)


def genre_detail(request, genre_id):
    genre_info = get_object_or_404(GenreTag, id=genre_id)
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

    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(user_id=request.user.id)
        favorite_tracks = user_info.track_set.all()
        context['favorite_tracks'] = favorite_tracks

    return render(request, 'kAboom/track_index.html', context)


def track_detail(request, track_id):
    track_details = get_object_or_404(Track.objects.select_related('artist', 'album', 'media_type'), id=track_id)
    duration = f'{track_details.milliseconds // 1000 // 60}:{track_details.milliseconds // 1000 % 60} мин'

    context = {
        'duration': duration,
        'track_details': track_details,
    }

    if request.user.is_authenticated:
        track_is_favorite = track_details.favorite.filter(user=request.user).exists()

        context['track_is_favorite'] = track_is_favorite

    return render(request, 'kAboom/track_detail.html', context)


def album_index(request):
    album_list = Album.objects.all()
    paginator = Paginator(album_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(user_id=request.user.id)
        favorite_albums = user_info.album_set.all()
        context['favorite_albums'] = favorite_albums

    return render(request, 'kAboom/album_index.html', context)


def album_detail(request, album_id):
    album_info = get_object_or_404(Album, id=album_id)
    track_list = Track.objects.filter(album_id=album_id)
    artist_info = Artist.objects.get(id=album_info.artist_id)
    context = {
        'MB': '',
        'artist_info': artist_info,
        'album_info': album_info,
        'track_list': track_list,
    }
    if request.user.is_authenticated:
        album_is_favorite = album_info.favorite.filter(user=request.user).exists()

        context['album_is_favorite'] = album_is_favorite
    return render(request, 'kAboom/album_detail.html', context)


def playlist_index(request):
    playlists = Playlist.objects.all()
    paginator = Paginator(playlists, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        user_info = UserProfile.objects.get(user_id=user_id)
        favorite_playlists = user_info.playlist_set.all()
        owners = playlists.filter(user_maker_id=user_id)

        context['owners'] = owners
        context['favorite_playlists'] = favorite_playlists

    return render(request, 'kAboom/playlist_index.html', context=context)


def playlist_detail(request, playlist_id):
    playlist_info = get_object_or_404(
        Playlist.objects.select_related('user_maker').prefetch_related('track'),
        id=playlist_id)
    track_list = playlist_info.track.all()
    paginator = Paginator(track_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'playlist_info': playlist_info,
        'track_list': track_list,
    }

    if request.user.is_authenticated:
        playlist_is_favorite = playlist_info.favorite.filter(user=request.user).exists()
        owner = playlist_info.user_maker_id == request.user.id

        context['playlist_is_favorite'] = playlist_is_favorite
        context['owner'] = owner

    return render(request, 'kAboom/playlist_detail.html', context=context)


@login_required
@require_POST
def playlist_delete(request):
    Playlist.objects.get(id=request.POST['playlist_id']).delete()
    return redirect(reverse('kAboom:my_playlists'))


@login_required
def playlist_creation(request):
    if request.method == 'POST':
        name = request.POST['name']
        new_playlist = Playlist(name=name, user_maker_id=request.user.id)
        new_playlist.save()
        playlist_id = new_playlist.id
        return redirect('kAboom:playlist_detail', playlist_id=playlist_id)
    return render(request, 'kAboom/playlist_creation.html')


@login_required
def my_playlists(request):
    playlists = Playlist.objects.filter(user_maker_id=request.user.id)
    context = {
        'playlists': playlists,
    }
    return render(request, 'kAboom/my_playlists.html', context)


@login_required
def change_playlist(request, playlist_id):
    track_list = Playlist.objects.get(id=playlist_id).track.all()
    favorite_tracks = UserProfile.objects.get(user_id=request.user.id).track_set.all()
    context = {
        'playlist_id': playlist_id,
        'track_list': track_list,
        'favorite_tracks': favorite_tracks,
    }
    return render(request, 'kAboom/change_playlist.html', context)


@login_required
@require_POST
def change_playlist_view(request):
    playlist_details = Playlist.objects.get(id=request.POST['playlist_id'])
    track_details = Track.objects.get(id=request.POST['track_id'])

    if request.POST['fav'] == 'rem':
        playlist_details.track.remove(track_details)
    elif request.POST['fav'] == 'add':
        playlist_details.track.add(track_details)

    return redirect(request.META.get('HTTP_REFERER', '/'))


def search(request, search_text):
    tracks_found = Track.objects.filter(name__icontains=search_text)

    context = {
        'search_text': search_text,
        'tracks_found': tracks_found
    }

    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(user_id=request.user.id)
        favorite_tracks = user_info.track_set.all()
        context['favorite_tracks'] = favorite_tracks

    return render(request, 'kAboom/search.html', context)


@require_POST
def track_search(request):
    return redirect('kAboom:search', search_text=request.POST['search_text'])


@require_POST
def switch_theme(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user_id=request.user.id)
        if request.session['theme'] == UserProfile.DARK:
            user.type_of_theme = UserProfile.LIGHT
            user.save()
            request.session['theme'] = UserProfile.LIGHT
        else:
            user.type_of_theme = UserProfile.DARK
            user.save()
            request.session['theme'] = UserProfile.DARK
    else:
        if 'theme' in request.session:
            if request.session['theme'] == UserProfile.DARK:
                request.session['theme'] = UserProfile.LIGHT
            else:
                request.session['theme'] = UserProfile.DARK
        else:
            request.session['theme'] = UserProfile.LIGHT
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def parsing(request, name):
    if not request.user.is_staff:
        return redirect('kAboom:main')
    all_tracks_list = Track.objects.values_list('name', flat=True)
    data = cache.get(f'data_{name}')
    if not data:
        parser = Parser.objects.get(name=name)
        url: str = parser.url
        function_name: str = parser.function_name
        data = FUNCTIONS[function_name](url)
        cache.set(f'data_{name}', data, 60*5)
    context = {
        'name': name,
        'data': data,
        'all_tracks': all_tracks_list
    }
    return render(request, 'kAboom/parsing.html', context)


@require_POST
def add_track(request):
    partner_name = request.POST['partner_name']
    media_format = request.POST['format']
    track_name = request.POST['track_name']
    if Track.objects.filter(name=track_name).exists():
        return redirect('kAboom:new_view')
    artist_name = request.POST['artist_name']
    genres = request.POST['genres_tags']
    genres_split = genres.split(', ')
    duration = request.POST['duration']
    size = request.POST['size']
    duration_split = duration.split(':')
    duration_in_milliseconds = int(duration_split[0]) * 60000 + int(duration_split[1]) * 1000
    size_split = size.split(' ')
    size_bytes = 0
    if size_split[1] == 'Mб' or size_split[1] == 'Мб':
        size_bytes = float(size_split[0]) * 1000000

    if not Artist.objects.filter(name=artist_name).exists():
        new_artist = Artist.objects.create(name=artist_name)
    else:
        new_artist = Artist.objects.get(name=artist_name)

    if not MediaType.objects.filter(name=media_format).exists():
        media_type = MediaType(name=media_format)
    else:
        media_type = MediaType.objects.get(name=media_format)

    new_track = Track.objects.create(
        name=track_name,
        artist=new_artist,
        milliseconds=duration_in_milliseconds,
        bytes=size_bytes,
        media_type=media_type,
    )
    for genre_name in genres_split:
        if not GenreTag.objects.filter(name=genre_name).exists():
            genre = GenreTag.objects.create(name=genre_name)
        else:
            genre = GenreTag.objects.get(name=genre_name)
        new_track.genre_tag.add(genre)
    return redirect('kAboom:parsing', name=partner_name)


def partner(request):
    parser_objects = Parser.objects.all()
    context = {
        'parser_objects': parser_objects
    }
    return render(request, 'kAboom/partner.html', context)
