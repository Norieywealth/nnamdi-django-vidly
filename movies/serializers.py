from django.db.models import fields
from rest_framework import serializers
from .models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'number_in_stock',
                  'daily_rental_rate', 'date_released')
