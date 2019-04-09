from omdb import OMDBClient
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from impy.settings import OMDB_KEY
from movies_api.filters import MoviesFilterSet
from movies_api.models import Movie
from movies_api.serializers import MovieSerializer


class MovieViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows movies to be viewed.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_class = MoviesFilterSet

    def create(self, request, *args, **kwargs):
        try:
            title = request.data['title'].lower()
        except KeyError:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        client = OMDBClient(apikey=OMDB_KEY)
        response = client.title(title, media_type='movie')
        real_title = response['title']
        try:
            movie = Movie.objects.get(details__title=real_title)
            serializer = self.get_serializer(movie, data=request.data)
            http_status = status.HTTP_302_FOUND
        except Movie.DoesNotExist:
            setattr(self, 'omdb_response', response)
            serializer = self.get_serializer(data=request.data)
            http_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=http_status, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
