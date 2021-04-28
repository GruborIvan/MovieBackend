from django.urls import path
from myapi.views import MovieView,MovieViewByIndex,MovieGenreView,RegisterView,VisitNumberCount,FavoriteMovies

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('genres',MovieGenreView.as_view()),
    path('movies',MovieView.as_view()),
    path('movies/<int:pk>',MovieViewByIndex.as_view()),
    path('visits',VisitNumberCount.as_view()),
    path('favorite',FavoriteMovies.as_view()),
]