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
def registeView(request):
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
