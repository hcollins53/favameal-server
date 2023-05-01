from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    """Restaurant Model"""
    name = models.CharField(max_length=55, unique=True)
    address = models.CharField(max_length=255)
    favorites = models.ManyToManyField(User, through="FavoriteRestaurant")

    @property
    def is_favorite(self):
      return self.__is_favorite

    @is_favorite.setter
    def is_favorite(self, value):
        self.__is_favorite = value
    # TODO: establish a many-to-many relationship with User through the join model
    # TODO: Add a `is_favorite` custom property. Remember each JSON representation of a restaurant should have a `is_favorite` property. Not just the ones where the value is `true`.
