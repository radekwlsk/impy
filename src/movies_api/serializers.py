from datetime import datetime

from rest_framework import serializers

from movies_api.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True, required=True, allow_blank=False)

    class Meta:
        model = Movie
        exclude = ('created', 'last_modified', 'released', 'country', 'metascore', 'imdb_rating',)
        read_only_fields = ('tags', 'details',)

    def create(self, validated_data):
        tag = validated_data['title'].lower()
        response = self.context['view'].omdb_response
        released = datetime.strptime(response['released'], "%d %b %Y").date()
        movie = Movie(
            tags=[tag],
            released=released,
            country=response['country'],
            metascore=response['metascore'],
            imdb_rating=response['imdb_rating'],
            details=response
            )
        movie.save()
        return movie

    def update(self, movie, validated_data):
        tag = validated_data['title'].lower()
        if tag not in movie.tags:
            movie.tags += [tag]
        movie.save()
        return movie
