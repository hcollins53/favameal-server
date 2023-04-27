# Favameal

You are inheriting a partially implemented API application using Django and the Django REST Framework plugin. It's a community driven site where anyone can add a restaurant to the system, and adds meals to restaurants.

Think of a very small scale Zomato or Yelp style service.

## Learning Objectives

After implementing the features for this application, you should know that verbs in the URL can be implemented with the `@action` decorator on a method in a ViewSet.

After implementing the features for this application, you should know the difference between properties on models that get their values from the database, and custom properties that get their values from the logic in a ViewSet.

1. You should be able to identify a custom model property.
1. You should be able to understand that a custom model property is used to define properties on model instances that do not get their values from the database.
1. You should be able to implement a custom property on a database model.
1. You should be able to assign a value to a custom property in the logic of a ViewSet.
1. You should be able to identify a custom action on a ViewSet.
1. You should be able to understand when a custom action is needed on a ViewSet.
1. You should be able to know how to specify that a custom action is for an individual resource, and not the collection of resources.
1. You should be able to know how to specify which HTTP methods a custom action will support.

## Setup

1. Clone the repository to a directory of your choosing.
2. Start the virtual environment with `pipenv install && pipenv shell`
3. Load the migrations: `python3 manage.py migrate`
4. Load the fixtures: `python3 manage.py loaddata fixtures`
5. Consider creating a new user so you know what the password is. Then login with Postman or Thunder Client, so you can grab the auth token for the next part. You'll need to include it in your request header.
6. Verify that the current functionality _(list below)_ works.

## Current Capabilities

The current functionality includes the following actions.

### Restaurants

Restaurant entries are not tied to a user. Once a restaurant has been added by **any** user, another user cannot enter it again.

1. POST a new restaurant
1. GET a single restaurant
1. GET all restaurants

### Meals

Meal entries are not tied to a user. Once a restaurant meal has been added by **any** user, another user cannot enter it again.

1. POST a new meal assigned to a restaurant
1. GET a single meal
1. GET all meals

## New Features to Add

### Favorite a Restaurant

Users should be able to mark a restaurant as a favorite, and also remove that choice.

| Method | URL |
|--------|-----|
| POST | http://localhost:8080/restaurants/1/favorite  |
| DELETE | http://localhost:8080/restaurants/1/unfavorite  |

When the client requests all restaurants, or a single restaurant, each JSON representation of a restaurant should have a `is_favorite` property. The value of the property must be `true` if the current user has marked it as a favorite, and `false` if the user hasn't.

### Favorite a Meal

Users should be able to mark a meal as a favorite, and also remove that choice.

| Method | URL |
|--------|-----|
| POST | http://localhost:8080/meals/1/favorite  |
| DELETE | http://localhost:8080/meals/1/unfavorite  |

When the client requests all meals, or a single meal, each JSON representation of a meal should have a `is_favorite` property. The value of the property must be `true` if the current user has marked it as a favorite, and `false` if the user hasn't.

### Rate a Meal

Users should be able to rate a meal on a scale of 1 to 10, and also update that rating.

| Method | URL |
|--------|-----|
| POST | http://localhost:8080/meals/1/rate  |
| PUT | http://localhost:8080/meals/1/rate  |

> #### Request Body Example

```json
{
    "rating": 3
}
```

When the client requests all meals, or a single meal, each JSON representation of a meal should have a `rating` property. The value of the property must be the current user rating if the current user has rated it, and 0 if the user hasn't.

When the client requests all meals, or a single meal, each JSON representation of a meal should have an `avg_rating` property. The value of the property must be the average of all user ratings for the meal.
