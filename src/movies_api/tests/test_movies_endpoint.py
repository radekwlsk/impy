from datetime import date

import pytest
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.test import APIClient

from movies_api.models import Movie
from movies_api.serializers import MovieSerializer
from movies_api.tests.conftest import _movie_1, _movie_2, _movie_3

client = APIClient()


def fake_call_omdb(tag):
    if tag in ['foo', 'the', 'the foo']:
        return _movie_1['details']['title'], _movie_1['details']
    elif tag in ['bar', 'big bar', 'big']:
        return _movie_2['details']['title'], _movie_2['details']
    elif tag in ['lorem', 'ipsum', 'lorem ipsum']:
        return _movie_3['details']['title'], _movie_3['details']
    else:
        raise NotFound(f"no movie matching '{tag}' found")


class TestMovies(object):

    @pytest.fixture(autouse=True)
    def setup(self, db, movie_1, movie_2):
        pass

    @pytest.mark.django_db
    def test_get_movies(self):
        response = client.get('/movies/')
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        assert serializer.data == response.data
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_post_movies_empty_body_bad_request(self):
        data = dict()
        response = client.post('/movies/', data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_post_movies_empty_title_bad_request(self):
        data = {'title': ""}
        response = client.post('/movies/', data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_post_movies_existing_tag_found(self, mocker):
        patched_call_omdb_by_title = mocker.patch('movies_api.views.MovieViewSet.call_omdb')
        tag = _movie_1['tags'][0]
        data = {'title': tag}
        response = client.post('/movies/', data=data)
        movie = Movie.objects.get(tags__contains=[tag])
        serializer = MovieSerializer(movie)

        patched_call_omdb_by_title.assert_not_called()
        assert serializer.data == response.data
        assert response.status_code == status.HTTP_302_FOUND

    @pytest.mark.django_db
    def test_post_movies_existing_title_found(self, mocker):
        patched_call_omdb = mocker.patch('movies_api.views.MovieViewSet.call_omdb', side_effect=fake_call_omdb)
        title = _movie_2['details']['title']
        data = {'title': title}
        response = client.post('/movies/', data=data)
        movie = Movie.objects.get(details__title=title)
        serializer = MovieSerializer(movie)

        patched_call_omdb.assert_not_called()
        assert serializer.data == response.data
        assert response.status_code == status.HTTP_302_FOUND

    @pytest.mark.django_db
    def test_post_movies_created(self, mocker):
        patched_call_omdb = mocker.patch('movies_api.views.MovieViewSet.call_omdb', side_effect=fake_call_omdb)
        title = _movie_3['details']['title']
        data = {'title': title}
        response = client.post('/movies/', data=data)
        movie = Movie.objects.get(details__title=title)
        serializer = MovieSerializer(movie)

        patched_call_omdb.assert_called_once_with(title.lower())
        assert serializer.data == response.data
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_post_movies_not_found(self, mocker):
        patched_call_omdb = mocker.patch('movies_api.views.MovieViewSet.call_omdb', side_effect=fake_call_omdb)
        title = "This Movie Does Not Exists In External API's Database"
        data = {'title': title}
        response = client.post('/movies/', data=data)

        patched_call_omdb.assert_called_once_with(title.lower())
        assert response.status_code == status.HTTP_404_NOT_FOUND

