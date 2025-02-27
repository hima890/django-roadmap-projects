from django.db import models

# Create your models here.
class Task(models.Model):
    """
    Task model represents a task in the task manager application.
    Attributes:
        STATUS_CHOICES (list): A list of tuples representing the possible status values for a task.
        description (TextField): A text field to store the description of the task.
        title (CharField): A character field to store the title of the task with a maximum length of 100 characters.
        created_at (DateTimeField): A datetime field that stores the timestamp when the task was created. Automatically set on creation.
        update_at (DateTimeField): A datetime field that stores the timestamp when the task was last updated. Automatically updated on save.
        status (CharField): A character field to store the status of the task with choices defined in STATUS_CHOICES. Defaults to 'pending'.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    description = models.TextField()
    title = models.CharField(
        max_length=100,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    update_at = models.DateTimeField(
        auto_now=True,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
        )
