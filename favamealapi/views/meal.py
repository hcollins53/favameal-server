"""View module for handling requests about meals"""
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from favamealapi.models import Meal, MealRating, Restaurant
from favamealapi.views.restaurant import RestaurantSerializer
from django.db.models import Avg, Count, Q

class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Meal
        # TODO: Add 'user_rating', 'avg_rating', 'is_favorite' fields to MealSerializer
        fields = ('id', 'name', 'restaurant', 'favorite_meals', 'is_favorite', 'mealrating', 'user_rating', 'avg_rating')

class MealView(ViewSet):
    """ViewSet for handling meal requests"""

    def create(self, request):
        """Handle POST operations for meals

        Returns:
            Response -- JSON serialized meal instance
        """
        try:
            meal = Meal.objects.create(
                name=request.data["name"],
                restaurant=Restaurant.objects.get(
                    pk=request.data["restaurant"])
            )
            serializer = MealSerializer(meal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single meal

        Returns:
            Response -- JSON serialized meal instance
        """
        try:
            meal = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).get(pk=pk)
            
            
            
            meal.is_favorite = request.auth.user in meal.favorite_meals.all()
            try:
                rating_object = MealRating.objects.get(user=request.auth.user, meal=meal)
                meal.user_rating = rating_object.rating 
            except MealRating.DoesNotExist:
                meal.user_rating = {}
            meal.avg_rating = meal.avg_rating if meal.avg_rating is not None else 0
            serializer = MealSerializer(meal)
            return Response(serializer.data)
        except Meal.DoesNotExist as ex:
            return Response({"reason": ex.message}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to meals resource

        Returns:
            Response -- JSON serialized list of meals
        """
        meals = Meal.objects.annotate(
            avg_rating=Avg('mealrating__rating'),
            is_favorite=Count(
                'favorite_meals',
                filter=Q(favorite_meals=request.auth.user)
            )
            #user_rating=Count(
               # 'mealrating',
               # filter=Q(mealrating=request.auth.user.id)
            #) 
        ).all()
        
        for meal in meals:
            try:
                rating_object = MealRating.objects.get(user=request.auth.user, meal=meal)
                meal.user_rating = rating_object.rating 
            except MealRating.DoesNotExist:
                meal.user_rating = {}

        serializer = MealSerializer(meals, many=True)

        return Response(serializer.data)

    # TODO: Add a custom action named `rate` that will allow a client to send a
    #  POST and a PUT request to /meals/3/rate with a body of..
    #       {
    #           "rating": 3
    #       }
    # If the request is a PUT request, then the method should update the user's rating instead of creating a new one

    @action(methods=['post'], detail=True)
    def favorite(self, request, pk):
        meal = Meal.objects.get(pk=pk)
        meal.favorite_meals.add(request.auth.user)
        return Response({'message': 'Meal favorited'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def unfavorite(self, request, pk):
        meal = Meal.objects.get(pk=pk)
        meal.favorite_meals.remove(request.auth.user)
        return Response({'message': 'Meal unfavorited'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def rate(self, request, pk):
        meal = Meal.objects.get(pk=pk)
        rating_value = request.data.get('rating')
        user = request.auth.user
        mealrating = MealRating.objects.create(user=user, meal=meal, rating=rating_value)
        # meal.mealrating.add(meal_rating)
        return Response({'message': 'Meal rated'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=True)
    def updateRate(self, request, pk):
        meal = Meal.objects.get(pk=pk)
        mealrating = MealRating.objects.get(user=request.auth.user, meal=meal)
        mealrating.rating = request.data.get('rating')
        mealrating.save()
        return Response({'message': 'Meal rating updated'}, status=status.HTTP_204_NO_CONTENT)
   
    