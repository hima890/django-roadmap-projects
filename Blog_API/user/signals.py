from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .tasks import send_email_task


@receiver(post_save, User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Sends a welcome email to a new user upon creation.
    This function is intended to be used as a Django signal handler for the
    post_save signal of the User model. When a new user instance is created,
    it sends a welcome email to the user's email address.
    Args:
        sender (Model): The model class that sent the signal.
        instance (User): The actual instance being saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.
    Returns:
        None
    """

    # Only of new user instande crated
    if created:
        subject = 'Welcome to Our Service'
        template_name = 'test'
        context = {
            'user_name': str(instance.first_name),
            'confirmation_link': 'https://test.test'
        }
        recipient_list = [str(instance.email)]
        attachments = None
        # Call Celery task asynchronously
        send_email_task.delay(subject, template_name, context, recipient_list, attachments)
    else:
        print('No email sent')
