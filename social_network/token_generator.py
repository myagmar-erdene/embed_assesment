import logging
import hashlib

from rest_framework.authtoken.models import Token


def create_or_update_auth_token(user):
    """
    Creates or updates the authentication Token for the User

    Args:
        user (request.user): The User

    Returns:
        None.
    """
    try:
        token = Token.objects.filter(user=user)

        if not token:
            # Create a new authentication token
            token = Token.objects.get_or_create(user=user)
        else:
            # Update an existing authentication token
            token = Token.objects.filter(user=user)
            new_key = token[0].generate_key()

            # Encrypt random string using SHA1
            sha1_algorithm = hashlib.sha1()
            sha1_algorithm.update(new_key.encode('utf-8'))
            first_level_value = sha1_algorithm.hexdigest()

            # Encrypt random string using MD5
            md5_algorithm = hashlib.md5()
            md5_algorithm.update(first_level_value.encode('utf-8'))
            second_level_value = md5_algorithm.hexdigest()

            token.update(key=second_level_value)
        return token

    except Exception as e:
        logging.error(
            msg=f'Failed to create auth token {e}',
            stacklevel=logging.CRITICAL
        )
