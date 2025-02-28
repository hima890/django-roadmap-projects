from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import User
from .utility import generate_jwt_tokens


@api_view(['POST'])
@permission_classes([AllowAny])  # Only authenticated users can access
def registeView(request):
    """
    Handle user registration.
    This view handles the registration of a new user. It checks if a user with the provided email
    already exists. If the user exists, it returns a 400 Bad Request response with an appropriate
    message. If the user does not exist, it validates the provided data using the UserSerializer.
    If the data is valid, it saves the new user and returns a 201 Created response with a success
    message and the user data. If the data is not valid, it returns a 400 Bad Request response with
    an error message and the validation errors.
    Args:
        request (HttpRequest): The HTTP request object containing the user data.
    Returns:
        Response: An HTTP response with a status code and a message indicating the result of the
        registration process.
    """
    
    serializer = UserSerializer(data=request.data)
    if User.objects.filter(email=request.data['email']).exists():
        return Response(
            {
                'message': 'User already exists.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'message': 'User created successfully.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {
                'message': 'User creation failed.',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])  # Only authenticated users can access
def login(request):
    """
    Handle user login by authenticating credentials and generating JWT tokens.
    Args:
        request (HttpRequest): The HTTP request object containing user credentials.
    Returns:
        Response: A DRF Response object containing a success message and JWT tokens if authentication is successful,
                  or an error message if authentication fails.
    """
    
    # Get the user credentials from the request
    email = request.data['email']
    password = request.data['password']

    # Authenticate the user
    user = authenticate(request, email=email, password=password)
    # If the user is not authenticated, return an error response
    if not user:
        return Response(
            {
                'message': 'Invalid credentials.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generate JWT tokens for the authenticated user
    access_token, refresh_token = generate_jwt_tokens(user)
    return Response(
        {
            'message': 'Login successful.',
            'access_token': access_token,
            'refresh_token': refresh_token
        },
        status=status.HTTP_200_OK
    )
