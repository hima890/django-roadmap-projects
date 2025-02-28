from django.db import models

# Create your models here.
class User(models.Model):
    """
    User model representing a user in the Blog API.
    Attributes:
        name (CharField): The name of the user, with a maximum length of 100 characters.
        email (EmailField): The email address of the user.
        password (CharField): The password of the user, with a maximum length of 50 characters.
        is_active (BooleanField): Indicates whether the user is active. Defaults to True.
        is_staff (BooleanField): Indicates whether the user has staff privileges. Defaults to False.
        created_at (DateTimeField): The date and time when the user was created. Automatically set on creation.
        updated_at (DateTimeField): The date and time when the user was last updated. Automatically set on update.
    Methods:
        __str__(): Returns the string representation of the user, which is the user's name.
    """
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name