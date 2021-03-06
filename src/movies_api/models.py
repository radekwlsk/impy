from django.contrib.postgres.fields import JSONField, ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.functions import DenseRank


class MovieManager(models.Manager):
    def comments_ranking(self, from_date, to_date):
        return self.annotate(
            total_comments=models.Count(
                models.Case(
                    models.When(comments__created__range=(from_date, to_date), then=1),
                    output_field=models.IntegerField(),
                )
            )
        ).annotate(
            rank=models.Window(
                expression=DenseRank(), order_by=models.F('total_comments').desc()
            )
        )


class Movie(models.Model):
    tags = ArrayField(
        models.CharField(max_length=128, unique=True)
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    details = JSONField(encoder=DjangoJSONEncoder)

    released = models.DateField(null=True)
    country = models.CharField(max_length=64, null=True)
    metascore = models.PositiveSmallIntegerField(null=True)
    imdb_rating = models.FloatField(null=True)

    objects = MovieManager()

    def __str__(self):
        return self.details['title']


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=256)
    created = models.DateField(auto_now_add=True)
