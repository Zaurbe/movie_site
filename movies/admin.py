# movies/admin.py
from django.contrib import admin
from .models import Actor, Director, Film, FilmRating, Review, Comment, Message

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'country', 'duration', 'director', 'kinopoisk_rating', 'imdb_rating')
    list_filter = ('year', 'country')

@admin.register(FilmRating)
class FilmRatingAdmin(admin.ModelAdmin):
    list_display = ('film', 'user', 'rating', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('film', 'user', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
