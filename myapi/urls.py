from django.urls import path
from myapi.views import MovieView,MovieViewByIndex

urlpatterns = [
    path('movies',MovieView.as_view()),
    path('movies/<int:pk>',MovieViewByIndex.as_view())
]