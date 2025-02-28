from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from .userManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model that extends AbstractBaseUser and PermissionsMixin.
    Fields:
        email (EmailField): Unique email address used as the username.
        first_name (CharField): User's first name with a maximum length of 50 characters.
        last_name (CharField): User's last name with a maximum length of 50 characters.
        is_active (BooleanField): Indicates whether the user account is active. Defaults to True.
        is_staff (BooleanField): Indicates whether the user has admin access. Defaults to False.
    Attributes:
        USERNAME_FIELD (str): Field used as the unique identifier for the user. Set to 'email'.
        REQUIRED_FIELDS (list): List of fields required when creating a superuser. Includes 'first_name' and 'last_name'.
    Methods:
        __str__: Returns the user's email address as the string representation of the user.
    """
    
    # Set the user table fields
    email = models.EmailField(unique=True)  # Use email instead of username
    first_name = models.CharField(max_length=50, default="Unknown")
    last_name = models.CharField(max_length=50, default="Unknown")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access    

    # Set the user groups and permissions
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    # Set the user manager model
    objects = UserManager()
    # Those line for the create superuser command 
    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Required when creating superusers

    def __str__(self):
        return self.email
