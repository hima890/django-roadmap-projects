import os
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
    The profile picture is an optional field and must be an image file with one of the
    following extensions: jpg, jpeg, png. The maximum allowed size for the profile picture
    is 5MB.
    Attributes:
        profile_picture (serializers.ImageField): Optional field for uploading a profile picture.
    Meta:
        model (User): The model associated with this serializer.
        fields (list): List of fields to be included in the serializer. Excludes email and password.
    Methods:
        validate_profile_image(image):
            Validates the profile image to ensure it has an allowed extension and does not exceed
            the maximum size limit.
            Args:
                image (File): The image file to be validated.
            Raises:
                serializers.ValidationError: If the image has an unsupported extension or exceeds
                the maximum size limit.
            Returns:
                File: The validated image file.
    """
    
    profile_picture = serializers.ImageField(required=False)  # Optional field for uploads

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture']  # Exclude email & password

    def  validate_profile_image(self, image):
        allowed_image_extensions = ['jpg', 'jpeg', 'png']
        allowed_image_size = 5 * 1024 * 1024 # 5MB

        image_extensions = os.path.splitext(image.name)[1][1:].lower()
        if image_extensions not in allowed_image_extensions:
            raise serializers.ValidationError(
                'Unsupported file extension. Supported extensions are jpg, jpeg, and png.'
            )

        if image.size > allowed_image_size:
            raise serializers.ValidationError(
                'The image size is too large. The maximum image size is 5MB.'
            )
        return image
