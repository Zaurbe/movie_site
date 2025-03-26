# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Film, Actor, Director, FilmRating, Review, Comment, Message
from .forms import RatingForm, ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.contrib.auth.models import User

def film_list(request):
    films = Film.objects.all()

    # Поиск по названию, году, стране, режиссеру, актеру
    query = request.GET.get('q')
    if query:
        films = films.filter(title__icontains=query)  # можно добавить и другие фильтры через Q-объекты

    # Фильтрация/сортировка
    sort_by = request.GET.get('sort')
    if sort_by == 'year_desc':
        films = films.order_by('-year')
    elif sort_by == 'year_asc':
        films = films.order_by('year')
    elif sort_by == 'kinopoisk_desc':
        films = films.order_by('-kinopoisk_rating')
    elif sort_by == 'kinopoisk_asc':
        films = films.order_by('kinopoisk_rating')
    elif sort_by == 'imdb_desc':
        films = films.order_by('-imdb_rating')
    elif sort_by == 'imdb_asc':
        films = films.order_by('imdb_rating')
    elif sort_by == 'user_desc':
        films = films.order_by('-user_rating')
    elif sort_by == 'user_asc':
        films = films.order_by('user_rating')
    elif sort_by == 'popularity':
        films = films.annotate(num_ratings=Count('ratings')).order_by('-num_ratings')

    context = {'films': films}
    return render(request, 'movies/film_list.html', context)

def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    reviews = film.reviews.all()
    # Можно добавить форму для добавления рецензии/комментария
    context = {'film': film, 'reviews': reviews}
    return render(request, 'movies/film_detail.html', context)

def actor_profile(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    films = actor.film_set.all()
    context = {'actor': actor, 'films': films}
    return render(request, 'movies/actor_profile.html', context)

def director_profile(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    films = director.film_set.all()
    context = {'director': director, 'films': films}
    return render(request, 'movies/director_profile.html', context)

@login_required
def user_profile(request, user_id):
    # Здесь можно получить профиль пользователя и его активность
    user = get_object_or_404(User, id=user_id)
    user_ratings = FilmRating.objects.filter(user=user)
    user_reviews = Review.objects.filter(user=user)
    context = {'profile_user': user, 'ratings': user_ratings, 'reviews': user_reviews}
    return render(request, 'movies/user_profile.html', context)

@login_required
def rate_film(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            film_rating, created = FilmRating.objects.update_or_create(
                film=film,
                user=request.user,
                defaults={'rating': rating_value}
            )
            # Пересчитываем общий рейтинг фильма
            agg = FilmRating.objects.filter(film=film).aggregate(avg_rating=Avg('rating'), count=Count('rating'))
            film.user_rating = agg['avg_rating']
            film.user_rating_count = agg['count']
            film.save()
            return redirect('movies:film_detail', film_id=film.id)
    else:
        form = RatingForm()
    return render(request, 'movies/rate_film.html', {'form': form, 'film': film})

@login_required
def add_review(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.film = film
            review.save()
            return redirect('movies:film_detail', film_id=film.id)
    else:
        form = ReviewForm()
    return render(request, 'movies/add_review.html', {'form': form, 'film': film})

@login_required
def add_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
            return redirect('movies:film_detail', film_id=review.film.id)
    else:
        form = CommentForm()
    return render(request, 'movies/add_comment.html', {'form': form, 'review': review})

@login_required
def chat(request):
    # Простейшая реализация чата: выводим список сообщений между пользователями
    # Здесь можно реализовать фильтрацию по отправителю/получателю, сортировку и т.д.
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    context = {'messages': messages}
    return render(request, 'movies/chat.html', context)
