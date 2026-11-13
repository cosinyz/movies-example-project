from django.urls import path

from . import views

urlpatterns = [
    path('top/', views.top_movies, name='movie-top'),
    path('', views.movie_list, name='movie-list'),
    path('<int:pk>/', views.movie_detail, name='movie-detail'),
]
