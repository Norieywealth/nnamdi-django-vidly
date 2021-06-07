import re
from django.core import paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Genre, Movie

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import GenreSerializer, MovieSerializer

from django.contrib.auth.decorators import login_required
# Create your views here.

# General Movies Page


@login_required(login_url='accounts:login')
def index(request):
    movie_fields = Movie._meta.fields
    genres = Genre.objects.all().order_by('name')

    if request.method == 'POST':
        column_name = request.POST['column_name']
        order = request.POST.get('order')
        if order == 'ASC':
            movies = Movie.objects.all().order_by(column_name)
        elif order == 'DESC':
            movies = Movie.objects.all().order_by('-'+column_name)

    else:
        movies = Movie.objects.all().order_by('title')
    count = movies.count()
    if count > 0:
        messages.success(request, f'There are {count} movies in the database')

    context = {
        'movies': movies,
        'movie_fields': movie_fields,
        'genres': genres

    }
    return render(request, 'movies/index.html', context)


@login_required(login_url='accounts:login')
def liked(request, id):
    movie = Movie.objects.get(pk=id)
    if movie.liked == True:
        movie.liked = False
    else:
        movie.liked = True
    movie.save()
    return redirect('/movies/')


@login_required(login_url='accounts:login')
def filter(request, genre):
    movie_fields = Movie._meta.fields
    if Movie.objects.filter(genre=genre).exists():
        if genre == '0':
            movies = Movie.objects.all().order_by('title')
        else:
            movies = Movie.objects.filter(genre=genre)
    else:
        movies = Movie.objects.all().order_by('title')
        if genre != 0:
            messages.success(request, 'No records found for this filter')

    genres = Genre.objects.all().order_by('name')
    context = {
        'movies': movies,
        'genres': genres,
        'movie_fields': movie_fields
    }
    return render(request, 'movies/index.html', context)
# Movies Functions


@login_required(login_url='accounts:login')
def movies(request):
    # return HttpResponse("Movies Management Page")
    if request.method == 'POST':
        title = request.POST.get('title')
        genre_id = request.POST.get('genre')
        stock = request.POST.get('stock')
        rate = request.POST.get('rate')
        year = request.POST.get('year')

        if Movie.objects.filter(title=title).exists():
            messages.success(request, 'Movie Exists!')
        else:
            genre = Genre.objects.get(id=genre_id)
            Movie.objects.create(
                title=title,
                genre=genre,
                number_in_stock=stock,
                daily_rental_rate=rate,
                date_released=year
            )
            messages.success(request, 'Movie Added!')
        return redirect('/movies/movies')
    else:
        movies = Movie.objects.all().order_by('title')
        count = movies.count()
        genres = Genre.objects.all().order_by('name')
        paginator = Paginator(movies, per_page=5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        if count > 0:
            messages.success(
                request, f'There are {count} movies in the database')

        context = {'genres': genres, 'movies': page_obj.object_list,
                   'page_number': int(page_number), 'paginator': paginator}
        return render(request, 'movies/movies.html', context)


@login_required(login_url='accounts:login')
def edit_movie(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre_id = request.POST.get('genre')
        stock = request.POST.get('stock')
        rate = request.POST.get('rate')
        year = request.POST.get('year')

        if Movie.objects.filter(title=title).exists():
            messages.success(request, 'Movie Exists!')
            return redirect(f'/movies/edit_movie/{id}')
        else:
            movie = Movie.objects.get(pk=id)
            genre = Genre.objects.get(id=genre_id)
            movie.title = title
            movie.genre = genre
            movie.number_in_stock = stock
            movie.daily_rental_rate = rate
            movie.date_released = year
            movie.save()
            messages.success(request, 'Movie Updated!')
        return redirect('/movies/movies')
    else:
        movie = get_object_or_404(Movie, pk=id)
        genres = Genre.objects.all().order_by('name')
        context = {'movie': movie, 'genres': genres}
        return render(request, 'movies/edit_movie.html', context)


@login_required(login_url='accounts:login')
def delete_movie(request, id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=id)
        movie.delete()
        messages.success(request, 'Movie Deleted!')
        return redirect('/movies/movies')
    else:
        movie = Movie.objects.get(id=id)
        context = {'movie': movie}
        return render(request, 'movies/delete_movie.html', context)

# Movie API


class MovieList(APIView):
    def get(self, request):
        movie_query = Movie.objects.all().order_by('title')
        serializer = MovieSerializer(movie_query, many=True)
        return Response(serializer.data)


# Genre Functions

@login_required(login_url='accounts:login')
def genres(request):
    # return HttpResponse("Genre Mangement Page")
    if request.method == 'POST':
        name = request.POST.get('name')
        if Genre.objects.filter(name=name).exists():
            messages.success(request, 'Genre already exists')
        else:
            Genre.objects.create(
                name=name
            )
            messages.success(request, 'Genre Added!')
        return redirect('/movies/genres')

    else:
        genres = Genre.objects.all().order_by('name')
        count = genres.count()
        paginator = Paginator(genres, per_page=5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        if count > 0:
            messages.success(
                request, f'There are {count} genres in the database')

        context = {'genres': page_obj.object_list, 'paginator': paginator,
                   'page_number': int(page_number)}
        return render(request, 'movies/genres.html', context)


@login_required(login_url='accounts:login')
def edit_genre(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Genre.objects.filter(name=name).exists():
            messages.success(request, 'Genre Exists!')
            return redirect(f'/movies/edit_genre/{id}')
        else:
            genre = get_object_or_404(Genre, id=id)
            genre.name = request.POST.get('name')
            genre.save()
            messages.add_message(request, messages.SUCCESS, 'Genre Updated!')
            return redirect('/movies/genres')
    else:
        genre = get_object_or_404(Genre, id=id)
        context = {'genre': genre}
        return render(request, 'movies/edit_genre.html', context)


@login_required(login_url='accounts:login')
def delete_genre(request, id):
    if request.method == 'POST':
        genre = get_object_or_404(Genre, id=id)
        genre.delete()
        messages.success(request, 'Genre Deleted!')
        return redirect('/movies/genres')
    else:
        genre = get_object_or_404(Genre, id=id)
        context = {'genre': genre}
        return render(request, 'movies/delete_genre.html', context)

# Genre API


class GenreList(APIView):
    def get(self, request):
        genre_query = Genre.objects.all().order_by('name')
        serializer = GenreSerializer(genre_query, many=True)
        return Response(serializer.data)
