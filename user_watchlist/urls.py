from django.urls import path
from user_watchlist.views import MovieListView,MovieListRemoveView

urlpatterns = [
    path('movielist',MovieListView.as_view()),
    path('movielist/<int:pk>',MovieListRemoveView.as_view()),
]