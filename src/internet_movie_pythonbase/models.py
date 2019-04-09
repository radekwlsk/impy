from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    details = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
