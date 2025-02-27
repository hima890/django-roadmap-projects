from rest_framework import serializers
from .models import user


class userSerializer(serializers.ModelSerializer):
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
        model = user
        fields = '__all__'

    def create(self, validated_data):
        # Use the create user method to hash and set the password then create the user
        return user.objects.create_user(**validated_data)
