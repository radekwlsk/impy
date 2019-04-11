from datetime import date

import pytest

from movies_api.models import Movie, Comment

_movie_1 = dict(
    tags=['foo'],
    details={
        'title': 'The Foo',
        'released': '12 Dec 2000',
        'country': 'USA',
        'metascore': '89',
        'imdb_rating': '7.5'
    },
    released=date(day=12, month=12, year=2000),
    country='USA',
    metascore=89,
    imdb_rating=7.5
)

_movie_2 = dict(
    tags=['bar'],
    details={
        'title': 'Bar',
        'released': '1 Jan 1990',
        'country': 'Poland',
        'metascore': '42',
        'imdb_rating': '4.2'
    },
    released=date(day=1, month=1, year=1990),
    country='Poland',
    metascore=42,
    imdb_rating=4.2
)

_movie_3 = dict(
    tags=['lorem'],
    details={
        'title': 'Lorem Ipsum',
        'released': '26 Apr 2014',
        'country': 'Singapore',
        'metascore': '99',
        'imdb_rating': '9.9'
    },
    released=date(day=26, month=4, year=2014),
    country='Singapore',
    metascore=99,
    imdb_rating=9.9
)

_comment_1_1 = dict(
    text="This is a comment",
    created=date(day=1, month=1, year=2010)
)
_comment_1_2 = dict(
    text="This is another comment",
    created=date(day=1, month=1, year=2012)
)
_comment_2_1 = dict(
    text="Other movie's comment",
    created=date(day=31, month=12, year=2012)
)


@pytest.fixture
def movie_1():
    movie = Movie.objects.create(**_movie_1)
    return movie


@pytest.fixture
def comment_1_1(movie_1):
    comment = Comment.objects.create(movie_id=movie_1, text=_comment_1_1['text'])
    comment.created = _comment_1_1['created']
    comment.save()
    return comment


@pytest.fixture
def comment_1_2(movie_1):
    comment = Comment.objects.create(movie_id=movie_1, text=_comment_1_2['text'])
    comment.created = _comment_1_2['created']
    comment.save()
    return comment


@pytest.fixture
def movie_2():
    movie = Movie.objects.create(**_movie_2)
    return movie


@pytest.fixture
def comment_2_1(movie_2):
    comment = Comment.objects.create(movie_id=movie_2, text=_comment_2_1['text'])
    comment.created = _comment_2_1['created']
    comment.save()
    return comment


@pytest.fixture
def movie_3():
    movie = Movie.objects.create(**_movie_3)
    return movie
