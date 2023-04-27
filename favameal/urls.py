# pylint: disable=missing-module-docstring
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from favamealapi.views import register_user, login_user
from favamealapi.views import RestaurantView, MealView

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantView, 'restaurant')
router.register(r'meals', MealView, 'meal')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
