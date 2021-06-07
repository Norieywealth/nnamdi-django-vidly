from django.contrib import admin
from .models import Movie, Genre
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'number_in_stock',
                    'daily_rental_rate', 'date_released')
    exclude = ('date_created', )

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre,GenreAdmin)
