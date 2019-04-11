from datetime import time, datetime

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from movies_api.tests.conftest import _comment_1_1, _comment_1_2, _comment_2_1

client = APIClient()


class TestTopMovies:

    @pytest.fixture(autouse=True)
    def setup(self, db, movie_1, movie_2, movie_3, comment_1_1, comment_1_2, comment_2_1):
        pass

    @pytest.mark.django_db
    def test_get_top_no_date_range_bad_request(self):
        response = client.get('/top/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_get_top_filter_day(self, movie_1, comment_1_1):
        comment_1_1_date = comment_1_1.created.isoformat()
        response = client.get(f"/top/?from_date={comment_1_1_date}&to_date={comment_1_1_date}")

        for record in response.data:
            if record['movie_id'] == movie_1.pk:
                assert record['total_comments'] == 1
                assert record['rank'] == 1
            else:
                assert record['total_comments'] == 0
                assert record['rank'] == 2
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_top_filter_range(self, movie_1, movie_2, comment_1_2, comment_2_1):
        comment_1_2_date = comment_1_2.created.isoformat()
        comment_2_1_date = comment_2_1.created.isoformat()
        response = client.get(f"/top/?from_date={comment_1_2_date}&to_date={comment_2_1_date}")

        for record in response.data:
            if record['movie_id'] in [movie_1.pk, movie_2.pk]:
                assert record['total_comments'] == 1
                assert record['rank'] == 1
            else:
                assert record['total_comments'] == 0
                assert record['rank'] == 2
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_top_filter_wrong_format_bad_request(self, comment_1_2, comment_2_1):
        comment_1_2_date = comment_1_2.created.strftime('%d-%m-%Y')
        comment_2_1_date = comment_2_1.created.strftime('%d-%m-%Y')
        response = client.get(f"/top/?from_date={comment_1_2_date}&to_date={comment_2_1_date}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_get_top_filter_datetime_time_bad_request(self, comment_1_2, comment_2_1):
        comment_1_2_datetime = datetime.combine(comment_1_2.created, time.min).isoformat()
        comment_2_1_datetime = datetime.combine(comment_2_1.created, time.max).isoformat()
        response = client.get(f"/top/?from_date={comment_1_2_datetime}&to_date={comment_2_1_datetime}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
