from django_elasticsearch_dsl import Document, Integer, Text, search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from django_elasticsearch_dsl.registries import registry
from .models import Movie

@registry.register_document
class MovieIndex(Document):

    class Index: 
        name = 'movies'

    class Django:
        model = Movie
        fields = ['title','description','imageurl','number_of_page_visits']

    def prepare__id(self,obj):
        return obj.id