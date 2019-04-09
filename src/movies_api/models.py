from django.contrib.postgres.fields import JSONField, ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class Movie(models.Model):
    tags = ArrayField(
        models.CharField(max_length=64, unique=True)
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    details = JSONField(encoder=DjangoJSONEncoder)

    released = models.DateField(blank=True)
    country = models.CharField(max_length=16, blank=True)
    metascore = models.PositiveSmallIntegerField(blank=True)
    imdb_rating = models.FloatField(blank=True)

    def __str__(self):
        return self.details['title']


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
