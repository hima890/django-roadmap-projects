from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserUpdateSerializer
from .models import User
from .utility import generate_jwt_tokens


@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response(
            {
                'message': 'Email and password are required.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

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


@api_view(['POST'])
def logout(request):
    """
    Handle user logout by blacklisting the refresh token.
    Args:
        request (HttpRequest): The HTTP request object containing the refresh token.
    Returns:
        Response: A DRF Response object containing a success message if the refresh token is blacklisted,
                  or an error message if the refresh token is invalid or expired.
    """
    # The clint should delete the ccess token on the client side
    # Get the refresh token from the request
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response(
            {
                'message': 'Refresh token not provided.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Blacklist the refresh token
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {
                'message': 'Logout successful.'
            },
            status=status.HTTP_200_OK
        )
    except TokenError:
        return Response(
            {
                'message': 'Invalid or expired refresh token.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    """
    Handle user profile updates.
    This view function handles GET and PUT requests for updating user profiles.
    GET:
        - Returns the current user's profile data.
    PUT:
        - Updates the user's profile with the provided data.
        - If 'profile_picture' is included in the request files, it updates the user's profile picture.
        - Returns a success message and the updated profile data if the update is successful.
        - Returns validation errors if the update fails.
    Args:
        request (HttpRequest): The HTTP request object containing user data and method type.
    Returns:
        Response: A DRF Response object containing the serialized user data or error messages.
    """

    user = request.user
    if  request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
           if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']  # Save the image
                serializer.save()
                return Response(
                    {
                        "message": "Profile updated successfully",
                        "data": serializer.data
                    },
                    status=200
                )
        return Response(
            {
                "message": "Profile update failed",
                "errors": serializer.errors
            },
            status=400
        )
