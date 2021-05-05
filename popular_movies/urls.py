from django.urls import path
from user_watchlist.views import MovieListView,MovieListRemoveView
from popular_movies.views import PopularMoviesView

urlpatterns = [
    path('popular/',PopularMoviesView.as_view()),
]