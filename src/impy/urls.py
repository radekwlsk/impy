from django.urls import include, path
from rest_framework import routers
from movies_api import views

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'top', views.TopMoviesViewSet, basename='top')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
