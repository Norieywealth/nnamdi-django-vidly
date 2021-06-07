import django


from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movies, name='movies'),
    path('edit_movie/<int:id>', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:id>', views.delete_movie, name='delete_movie'),
    path('genres/', views.genres, name='genres'),
    path('edit_genre/<int:id>', views.edit_genre, name='edit_genre'),
    path('delete_genres/<int:id>', views.delete_genre, name='delete_genre'),
    path('liked/<int:id>', views.liked, name='liked'),
    path('filter/<int:genre>', views.filter, name="filter")


]
