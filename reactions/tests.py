from django.test import TestCase,Client
from myapi.models import Movie,MovieGenre
import json
from rest_framework import status
from .models import Reactions
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate,APIClient

# Create your tests here.
class LikeMovieTestCase(TestCase):
    
    def setUp(self):

        self.user = User(username="ivang@app.com")
        self.user.set_password('grugrugru')
        self.user.is_superuser = True
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.movie_genre = MovieGenre.objects.create(genre_name='Action')
        self.movie = Movie.objects.create(title='TestMovie1',description='TestDescription1',imageurl='Nothing1.jpg')
        self.movie.genre.set([self.movie_genre])

        self.reaction = {
            'movie' : 1,
            'reaction' : True
        }

    def test_add_like(self):
        response = self.client.post(path='/reactions',data=json.dumps(self.reaction),content_type='application/json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # This test is supposed to fail..
    def test_repeat_like(self):
        response = self.client.post(path='/reactions',data=json.dumps(self.reaction),content_type='application/json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)