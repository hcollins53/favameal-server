from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Login in existing users

    Args:
        request (Request): The incoming request from the client

    Returns:
        dict: Indicates if the user is valid, if so returns the user's token
    """
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
    else:
        data = {
            'valid': False
        }
    return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Registers a new user

    Args:
        request (Request): The incoming request from the client

    Returns:
        dict: The user's newly created token
    """
    user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    token = Token.objects.create(user=user)

    data = {
        'token': token.key
    }

    return Response(data)
