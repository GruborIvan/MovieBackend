from django.urls import path
from reactions.views import ReactionsView,CommentsView

urlpatterns = [
    path('reactions',ReactionsView.as_view()),
    path('comments',CommentsView.as_view()),
]