from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from .userManager import UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model that extends AbstractBaseUser and PermissionsMixin.
    Fields:
        email (EmailField): Unique email address used as the username.
        first_name (CharField): User's first name with a maximum length of 50 characters.
        last_name (CharField): User's last name with a maximum length of 50 characters.
        bio (TextField): Optional user biography.
        profile_picture (ImageField): Optional profile picture, uploaded to 'profile_pics/' directory.
        social_links (JSONField): Optional JSON field to store user's social media links.
        is_active (BooleanField): Indicates whether the user account is active.
        is_staff (BooleanField): Indicates whether the user has staff privileges.
        date_joined (DateTimeField): Timestamp when the user account was created.
        last_login (DateTimeField): Timestamp of the user's last login.
    Relationships:
        groups (ManyToManyField): Groups the user belongs to, related to the Group model.
        user_permissions (ManyToManyField): Permissions assigned to the user, related to the Permission model.
    Manager:
        objects (UserManager): Custom manager for the User model.
    Constants:
        USERNAME_FIELD (str): Field used as the unique identifier for the user (email).
        REQUIRED_FIELDS (list): List of fields required when creating a superuser (first_name, last_name).
    Methods:
        __str__(): Returns a string representation of the user, including email, first name, and last name.
    """
    
    # Set the user table fields
    email = models.EmailField(unique=True)  # Use email instead of username
    first_name = models.CharField(max_length=50, default="Unknown")
    last_name = models.CharField(max_length=50, default="Unknown")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    # Set the user groups and permissions
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    # Set the user manager model
    objects = UserManager()
    # Those line for the create superuser command 
    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Required when creating superusers

    def __str__(self):
        return "Email: {}, First Name: {}, Last Name: {}".format(
            self.email,
            self.first_name,
            self.last_name
        )
