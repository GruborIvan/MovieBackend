from django.urls import path
from reactions.views import ReactionsView

urlpatterns = [
    path('reactions',ReactionsView.as_view())
]