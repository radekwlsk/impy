from datetime import datetime

from rest_framework import serializers

from movies_api.models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True, required=True, allow_blank=False)

    class Meta:
        model = Movie
        exclude = ('created', 'last_modified', 'released', 'country', 'metascore', 'imdb_rating',)
        read_only_fields = ('tags', 'details', 'id')

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


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ('id',)
        read_only_fields = ('created',)

    def create(self, validated_data):
        comment = Comment(
            movie_id=validated_data['movie_id'],
            text=validated_data['text'],
        )
        comment.save()
        return comment


class TopMoviesSerializer(serializers.ModelSerializer):
    movie_id = serializers.SerializerMethodField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ('movie_id', 'total_comments', 'rank')

    @staticmethod
    def get_movie_id(obj):
        return obj.pk

    def update(self, instance, validated_data):
        pass
