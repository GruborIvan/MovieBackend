from reactions.models import Reactions,Comments
from reactions.serializers import ReactionsSerializer,CommentSerializer
from rest_framework import generics,status
from django.http import HttpResponse

class ReactionsView(generics.CreateAPIView):

    queryset = Reactions.objects.all()
    serializer_class = ReactionsSerializer

    def perform_create(self,serializer):
        try:
            serializer.save(user=self.request.user)
        except:
            item = Reactions.objects.filter(user=self.request.user).filter(movie=self.request.data.get("movie")).first()
            if item is not None:
                if item.reaction !=  self.request.data.get("reaction"):
                    item.reaction = self.request.data.get("reaction")
                    item.save()


class CommentsView(generics.ListCreateAPIView):

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None

    def get_queryset(self):
        return Comments.objects.filter(movie=self.request.GET.get('movie_id'))

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
