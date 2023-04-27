from django.contrib.auth.models import User
from django.db import models


class MealRating(models.Model):
    """Meal Rating model
    Holds the rating a user has given a meal
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mealrating")
    meal = models.ForeignKey(
        "Meal", on_delete=models.CASCADE, related_name="mealrating")
    rating = models.IntegerField()
