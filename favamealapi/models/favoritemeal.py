from django.contrib.auth.models import User
from django.db import models


class FavoriteMeal(models.Model):
    """Favorite Meal model
        Join model for the many to many relationship between user and meal
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userfavoritemeals")
    meal = models.ForeignKey(
        "Meal", on_delete=models.CASCADE, related_name="userfavoritemeals")
