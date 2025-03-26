# movies/urls.py
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.film_list, name='film_list'),
    path('film/<int:film_id>/', views.film_detail, name='film_detail'),
    path('actor/<int:actor_id>/', views.actor_profile, name='actor_profile'),
    path('director/<int:director_id>/', views.director_profile, name='director_profile'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('rate/<int:film_id>/', views.rate_film, name='rate_film'),
    path('review/<int:film_id>/', views.add_review, name='add_review'),
    path('comment/<int:review_id>/', views.add_comment, name='add_comment'),
    path('chat/', views.chat, name='chat'),
]
