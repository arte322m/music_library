from django.urls import path

from . import views

app_name = 'kAboom'
urlpatterns = [
    path('', views.index, name='index'),
    path('artist/<int:artist_id>/', views.album, name='album'),
    path('album/<int:album_id>/', views.track, name='track'),
]
