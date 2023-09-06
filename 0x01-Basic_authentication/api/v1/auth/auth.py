#!/usr/bin/env python3
"""Class module for authentication"""

from typing import List, TypeVar
from flask import request


class Auth:
    """Authentification class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if the path is not in the list of strings excluded_paths.

        Returns True if path is None.
        Returns True if excluded_paths is None or empty.
        Returns False if path is in excluded_paths.

        Assumes excluded_paths contain string paths always ending with a /.
        This method is slash tolerant.

        Args:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): List of excluded paths.

        Returns:
            bool: True if authentication is required, False otherwise.
        """

        # If path is None or excluded_paths is None/empty.
        if path is None or not excluded_paths:
            return True

        # Ensure path ends with a slash.
        if not path.endswith('/'):
            path += '/'

        # Check if path is in excluded_paths (slash tolerant).
        return not any(path.startswith(ex_path) for ex_path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """
        Validates the request and returns the value of the
        Authorization header if present.

        If request is None, returns None.
        If request doesn’t contain the header key Authorization,
        returns None.
        Otherwise, return the value of the header request Authorization.

        Args:
            request (Request): The Flask request object.

        Returns:
            str or None: The value of the Authorization header or
            None if not present.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method for current_user.
        """
        return None
