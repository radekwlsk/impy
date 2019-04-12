from datetime import date

from omdb import OMDBClient
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response

from impy.settings import OMDB_KEY
from movies_api.filters import MoviesFilterSet
from movies_api.models import Movie, Comment
from movies_api.serializers import MovieSerializer, CommentSerializer, TopMoviesSerializer


class BadQueryError(Exception):
    pass


class MovieViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows movies to be listed and added.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_class = MoviesFilterSet

    @staticmethod
    def call_omdb(tag):
        client = OMDBClient(apikey=OMDB_KEY)
        response = client.title(tag, media_type='movie')
        try:
            return response['title'], response
        except KeyError:
            raise NotFound(f"no movie matching \"{tag}\" found")

    @staticmethod
    def get_title(request):
        if 'title' not in request.data or request.data['title'] == "":
            raise ParseError("title required in request body")
        return request.data['title'].lower()

    def get_movie_or_response(self, tag):
        try:
            movie = Movie.objects.get(tags__contains=[tag])
            return movie, None
        except Movie.DoesNotExist:
            real_title, response = self.call_omdb(tag)
            try:
                movie = Movie.objects.get(details__title=real_title)
                return movie, None
            except Movie.DoesNotExist:
                return None, response

    def create(self, request, *args, **kwargs):
        tag = self.get_title(request)
        movie, response = self.get_movie_or_response(tag)
        serializer = self.get_serializer(movie, data=request.data)
        if movie is not None:
            http_status = status.HTTP_302_FOUND
        else:
            setattr(self, 'omdb_response', response)
            http_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=http_status, headers=headers)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    API endpoint that allows comments to be listed and added.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = ('movie_id', 'created')


class TopMoviesViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    API endpoint that allows listing top movies by comments.
    """
    serializer_class = TopMoviesSerializer

    def get_queryset(self):
        from_date_param = self.request.query_params.get('from_date')
        to_date_param = self.request.query_params.get('to_date')
        try:
            from_date = date.fromisoformat(from_date_param)
            to_date = date.fromisoformat(to_date_param)
        except (TypeError, ValueError):
            raise BadQueryError("from_date and to_date query parameters are required, format: YYYY-MM-DD")
        if from_date > to_date:
            raise BadQueryError("defined date range has to be positive")

        queryset = Movie.objects.comments_ranking(from_date, to_date)

        return queryset.order_by('rank').all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except BadQueryError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
