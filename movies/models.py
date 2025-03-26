# movies/models.py
from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='actors/', null=True, blank=True)

    def __str__(self):
        return self.name

    def personal_rating(self):
        # Рассчитываем рейтинг на основе оценок фильмов, где этот актер участвовал
        films = self.film_set.all()
        total = 0
        count = 0
        for film in films:
            if film.user_rating:
                total += film.user_rating
                count += 1
        return round(total / count, 1) if count else None

class Director(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='directors/', null=True, blank=True)

    def __str__(self):
        return self.name

    def personal_rating(self):
        # Рассчитываем рейтинг на основе оценок фильмов, где этот режиссер
        films = self.film_set.all()
        total = 0
        count = 0
        for film in films:
            if film.user_rating:
                total += film.user_rating
                count += 1
        return round(total / count, 1) if count else None

class Film(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    country = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Продолжительность в минутах")
    poster = models.ImageField(upload_to='posters/')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='film_set')
    actors = models.ManyToManyField(Actor, related_name='film_set')
    kinopoisk_rating = models.DecimalField(max_digits=3, decimal_places=1)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1)
    
    # Поле для хранения агрегированного пользовательского рейтинга и количества оценок.
    user_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    user_rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class FilmRating(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('film', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.film.title}: {self.rating}"

class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.film.title}"

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username}"

# Для личных сообщений можно создать модель чата
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"
