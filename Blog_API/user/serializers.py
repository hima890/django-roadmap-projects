from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    userSerializer is a ModelSerializer for the user model. It includes all fields of the user model and sets the password field to write-only with a minimum length of 6 characters.
    Attributes:
        password (serializers.CharField): A write-only field for the user's password with a minimum length of 6 characters.
    Methods:
        create(validated_data):
            Creates and returns a new user instance using the validated data.
    """
    
    # Set the password field to write-only
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        # Set the model o the user
        model = User
        # Set the fields to include in the serializer
        fields = [
            'id', 'email',
            'first_name',
            'last_name', 'password',
            'is_active', 'is_staff',
            'last_login'
        ]

    def create(self, validated_data):
        # Use the create user method to hash and set the password then create the user
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    This serializer allows updating the user's first name, last name, and profile picture.
    The profile picture field is optional.
    Attributes:
        profile_picture (serializers.ImageField): Optional field for uploading a profile picture.
    Meta:
        model (User): The model that this serializer is based on.
        fields (list): List of fields to be included in the serialization. 
                       It includes 'first_name', 'last_name', and 'profile_picture'.
    """

    profile_picture = serializers.ImageField(required=False)  # Optional field for uploads

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture']  # Exclude email & password
