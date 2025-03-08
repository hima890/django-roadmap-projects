from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.utils.timezone import now
from celery import shared_task
from .utility import send_email_with_attachments



@shared_task
def clean_expired_blacklisted_tokens():
    """
    Deletes expired blacklisted tokens from the database.
    This function queries the BlacklistedToken model to find all tokens
    that have expired (i.e., their expiration date is less than the current time).
    It then deletes these expired tokens and returns a message indicating
    the number of tokens that were deleted.
    Returns:
        str: A message indicating the number of expired blacklisted tokens deleted.
    """
    
    expired_tokens = BlacklistedToken.objects.filter(token__expires_at__lt=now())
    count = expired_tokens.count()
    expired_tokens.delete()
    return "Deleted {} expired blacklisted tokens.".format(count)


@shared_task
def send_email_task(subject, template_name, context, recipient_list, attachments=None):
    """
    Sends an email with the specified subject, template, context, and recipient list, optionally including attachments.
    Args:
        subject (str): The subject of the email.
        template_name (str): The name of the email template to use.
        context (dict): A dictionary of context variables to render the template.
        recipient_list (list): A list of recipient email addresses.
        attachments (list, optional): A list of file attachments to include in the email. Defaults to None.
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    
    return send_email_with_attachments(subject, template_name, context, recipient_list, attachments)
