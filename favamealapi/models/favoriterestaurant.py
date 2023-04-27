from django.contrib.auth.models import User
from django.db import models


class FavoriteRestaurant(models.Model):
    """Favorite Restaurant model
        Join model for the many to many relationship between user and restaurant
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userfavoriterestaurants")
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="userfavoriterestaurants")
