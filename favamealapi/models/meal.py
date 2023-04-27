from django.db import models


class Meal(models.Model):
    """Meal Model
    """
    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    # TODO: Establish a many-to-many relationship with User through the appropriate join model

    # TODO: Add an user_rating custom properties

    # TODO: Add an avg_rating custom properties
