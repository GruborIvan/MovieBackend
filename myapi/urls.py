from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapi.views import MovieView,MovieViewByIndex,MovieGenreView,RegisterView,VisitNumberCount,PopularMovies,ElasticSearchView,ImageRetrieve

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('genres',MovieGenreView.as_view()),
    path('movies',MovieView.as_view()),
    path('movies/<int:pk>',MovieViewByIndex.as_view()),
    path('visits',VisitNumberCount.as_view()),
    path('movies/popular',PopularMovies.as_view()),
    path('movies/elasticsearch',ElasticSearchView.as_view()),
    path('pics',ImageRetrieve.as_view()),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)