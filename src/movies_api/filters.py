from django.contrib.postgres.fields import ArrayField
from django_filters import FilterSet, BaseCSVFilter, CharFilter

from movies_api.models import Movie


class CharArrayFilter(BaseCSVFilter, CharFilter):
    pass


class MoviesFilterSet(FilterSet):

    class Meta:
        model = Movie
        fields = [
            'tags',
            'released',
            'country',
            'metascore',
            'imdb_rating'
        ]
        filter_overrides = {
            ArrayField: {
                'filter_class': CharArrayFilter,
                'extra': lambda f: {
                    'lookup_expr': 'contains',
                },
            }
        }
