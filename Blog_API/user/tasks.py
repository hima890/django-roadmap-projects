from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.utils.timezone import now


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
