#!/usr/bin/env python3
"""Password Hashing Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """Hash Password"""
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new uuid and return it as a string"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""

        try:
            # Try to find the user by email
            user = self._db.find_user_by(email=email)

            # Check if the provided password match the stoted hashed password
            password = password.encode('utf-8')
            if bcrypt.checkpw(password,
                              user.hashed_password):
                return True

        except NoResultFound:
            pass

        return False

    def create_session(self, email: str) -> str:
        """Create a session id for a user with the given email"""

        try:
            # Find the user corresponding to the email
            user = self._db.find_user_by(email=email)

            # Generate a new session ID using the _generate_uuid method
            session_id = _generate_uuid()

            # Update the user's session_id in the database
            self._db.update_user(user.id, session_id=session_id)

            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Retrieve a user data from its session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            else:
                return None

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user session with the given user_id"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Get a password reset token of a user with the given email"""

        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError("User does not exist")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password:str) -> None:
        """Update the new password for the user"""
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError('User does not exist')
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password = hashed_password,
                             reset_token = None)
