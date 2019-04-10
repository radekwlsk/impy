from datetime import date

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from movies_api.models import Movie
from movies_api.serializers import MovieSerializer

client = APIClient()


@pytest.mark.django_db
class TestMovies(object):

    @pytest.fixture(autouse=True)
    def setup(self, db):
        Movie.objects.get_or_create(
            tags=['foo', 'the foo'],
            details={
                'title': 'The Foo'
            },
            released=date(day=12, month=12, year=2000),
            country='USA',
            metascore=89,
            imdb_rating=7.5
        )
        Movie.objects.get_or_create(
            tags=['bar'],
            details={
                'title': 'Bar'
            },
            released=date(day=1, month=1, year=1990),
            country='Poland',
            metascore=42,
            imdb_rating=4.2
        )

    @pytest.mark.django_db
    def test_get_movies(self):
        response = client.get('/movies/')
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        assert serializer.data == response.data
        assert response.status_code == status.HTTP_200_OK
