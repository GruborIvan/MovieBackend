from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('',include('myapi.urls')),
    path('',include('user_watchlist.urls')),
    path('admin/', admin.site.urls),

    # JWT Authentication..
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]
