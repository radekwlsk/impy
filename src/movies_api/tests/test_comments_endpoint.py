import pytest
from rest_framework import status
from rest_framework.test import APIClient

from movies_api.models import Movie, Comment
from movies_api.serializers import CommentSerializer

client = APIClient()


class TestComments:

    @pytest.fixture(autouse=True)
    def setup(self, db, movie_1, movie_2, comment_1_1, comment_1_2, comment_2_1):
        pass

    @pytest.mark.django_db
    def test_get_comments(self):
        response = client.get('/comments/')
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        assert serializer.data == response.data
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_comments_filtered_movie_id(self):
        movie = Movie.objects.first()
        response = client.get(f'/comments/?movie_id={movie.pk}')
        comments = Comment.objects.filter(movie_id=movie.pk)
        serializer = CommentSerializer(comments, many=True)

        assert serializer.data == response.data
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_comments_filtered_date(self, comment_1_1):
        response = client.get(f"/comments/?created={comment_1_1.created.isoformat()}")
        comments = Comment.objects.filter(created=comment_1_1.created)
        serializer = CommentSerializer(comments, many=True)

        assert serializer.data == response.data
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_post_comment_created(self):
        movie = Movie.objects.first()
        data = {
            'movie_id': movie.pk,
            'text': "New and fresh comment"
        }
        response = client.post('/comments/', data=data)
        comment = Comment.objects.get(text=data['text'])
        serializer = CommentSerializer(comment)

        assert serializer.data == response.data
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_post_comment_empty_body_bad_request(self):
        data = dict()
        response = client.post('/comments/', data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_post_comment_wrong_movie_id_bad_request(self):
        last_id = Movie.objects.values_list('id', flat=True).order_by('id').last()
        wrong_id = last_id + 1
        data = {
            'movie_id': wrong_id,
            'text': "New and fresh comment"
        }
        response = client.post('/comments/', data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
