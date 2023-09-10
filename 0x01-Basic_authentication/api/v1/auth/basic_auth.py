#!/usr/bin/env python3
"""Basic Authentication Module"""

from api.v1.auth.auth import Auth
import models.user
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Returns Basic authentication"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the base64 string of the authentication header"""

        if not authorization_header or not isinstance(
                authorization_header, str):
            return None

        authorization_header = authorization_header.split()

        if len(authorization_header) != 2 or authorization_header[
                0] != "Basic":
            return None

        return authorization_header[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode base64 authorization authentication
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            # Attempt to decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)

            # Decode the bytes to a UTF-8 string
            decoded_string = decoded_bytes.decode('utf-8')

            return decoded_string
        except base64.binascii.Error:
            # Handle the case where decoding as Base64 fails
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded
        value.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        user_email, user_password = decoded_base64_authorization_header.split(
                ':', 1)
        return (user_email, user_password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        # Search for users with the given email in the database

        users = models.user.User.search({"email": user_email})
        if not users or users is None:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the User instance for a request.

        :param request: The Flask request object.
        :return: The User instance if authentication is successful,
        otherwise None.
        """
        if request is None:
            return None

        authorization_header = super().authorization_header(request)

        if authorization_header is None:
            return None

        base64_authorization = self.extract_base64_authorization_header(
                authorization_header)

        if base64_authorization is None:
            return None

        decoded_base64 = self.decode_base64_authorization_header(
                base64_authorization)

        if decoded_base64 is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                decoded_base64)

        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
