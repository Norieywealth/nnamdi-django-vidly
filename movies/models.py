from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.utils import timezone
# Create your models here.


class Genre(models.Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    number_in_stock = models.IntegerField()
    daily_rental_rate = models.FloatField()
    date_released = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    liked = models.BooleanField(default=False)
