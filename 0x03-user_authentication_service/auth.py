#!/usr/bin/env python3
"""Password Hashing Module"""
import bcrypt
from db import DB


def _hash_password(password: str) -> bytes:
    """Hash Password"""
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        args:
            email (str): The email of the new user
            passwor (str): The password of the new user.

        Returns:
            User: The User object for the newly registered user.

        Raises:
            ValueError: If the email already exist in the database
        """

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')

        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user
