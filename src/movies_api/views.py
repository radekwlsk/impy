from datetime import datetime, time, date

from django.db.models import Count, Window, F, Case, When, IntegerField
from django.db.models.functions import DenseRank
from omdb import OMDBClient
from rest_framework import viewsets, mixins, status
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

    def create(self, request, *args, **kwargs):
        try:
            title = request.data['title'].lower()
        except KeyError:
            return Response({"error": "title query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
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

        from_dt = datetime.combine(from_date, time.min)
        to_dt = datetime.combine(to_date, time.max)

        queryset = Movie.objects.annotate(
            total_comments=Count(
                Case(
                    When(comments__created__range=(from_dt, to_dt), then=1),
                    output_field=IntegerField(),
                )
            )
        ).annotate(
            rank=Window(expression=DenseRank(), order_by=F('total_comments').desc())
        )

        return queryset.order_by('rank').all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except BadQueryError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
