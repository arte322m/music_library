from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .Bsoup import trend_of_main_page
from .models import UserProfile, Album, Playlist, Artist, Track, Genre


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
    track_rating = Track.objects.annotate(num_favorite_tracks=Count('favorite')).order_by('-num_favorite_tracks')[:10]
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

    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(user_id=request.user.id)
        favorite_tracks = user_info.track_set.all()
        context['favorite_tracks'] = favorite_tracks

    return render(request, 'kAboom/track_index.html', context)


def track_detail(request, track_id):
    track_details = get_object_or_404(Track, id=track_id)
    album_info = track_details.album
    artist_info = album_info.artist

    context = {
        'track_details': track_details,
        'artist_info': artist_info,
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
    playlist_list = Playlist.objects.all()
    paginator = Paginator(playlist_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'playlist_list': playlist_list,
    }

    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(user_id=request.user.id)
        favorite_playlists = user_info.playlist_set.all()
        owners = Playlist.objects.filter(user_maker_id=request.user.id)

        context['owners'] = owners
        context['favorite_playlists'] = favorite_playlists

    return render(request, 'kAboom/playlist_index.html', context=context)


def playlist_detail(request, playlist_id):
    playlist_info = get_object_or_404(Playlist, id=playlist_id)
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


def new_view(request):
    data = trend_of_main_page()
    context = {
        'data': data
    }
    return render(request, 'kAboom/new_view.html', context)
