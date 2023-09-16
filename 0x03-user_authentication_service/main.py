#!/usr/bin/env python3
"""Test Module"""

import requests
from typing import Optional

# Replace with your actual server base URL
BASE_URL = "http://your_server_base_url_here"


def register_user(email: str, password: str) -> None:
    """
    Register a new user.

    Args:
        email (str): The email address for registration.
        password (str): The password for registration.

    Raises:
        AssertionError: If registration fails (status code is not 200).
    """
    url = f"{BASE_URL}/register"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200, "Registration failed."


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with an incorrect password.

    Args:
        email (str): The email address for login.
        password (str): An incorrect password.

    Raises:
        AssertionError: If login does not result in a 401 Unauthorized status.
    """
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401,
    "Expected 401 Unauthorized status code."


def log_in(email: str, password: str) -> str:
    """
    Log in and return the session ID.

    Args:
        email (str): The email address for login.
        password (str): The password for login.

    Returns:
        str: The session ID.

    Raises:
        AssertionError: If login fails (status code is not 200)
        or session ID is missing.
    """
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200, "Login failed."
    session_id = response.json().get("session_id")
    assert session_id is not None, "Session ID not found in response."
    return session_id


def profile_unlogged() -> None:
    """
    Attempt to access the profile without being logged in.

    Raises:
        AssertionError: If access does not result in a 403 Forbidden status.
    """
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, "Expected 403 Forbidden status code."


def profile_logged(session_id: str) -> None:
    """
    Access the user profile while logged in.

    Args:
        session_id (str): The session ID obtained during login.

    Raises:
        AssertionError: If profile access fails (status code is not 200).
    """
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, "Profile access failed."


def log_out(session_id: str) -> None:
    """
    Log out the user.

    Args:
        session_id (str): The session ID obtained during login.

    Raises:
        AssertionError: If log out fails (status code is not 302).
    """
    url = f"{BASE_URL}/logout"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 302, "Expected 302 Redirect status code."


def reset_password_token(email: str) -> str:
    """
    Request a reset password token.

    Args:
        email (str): The email address associated with the user.

    Returns:
        str: The reset password token.

    Raises:
        AssertionError: If the request for a reset token fails
        (status code is not 200) or token is missing.
    """
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200, "Reset password token request failed."
    reset_token = response.json().get("reset_token")
    assert reset_token is not None, "Reset token not found in response."
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the user's password using a reset token.

    Args:
        email (str): The email address associated with the user.
        reset_token (str): The reset password token.
        new_password (str): The new password to set.

    Raises:
        AssertionError: If password update fails (status code
        is not 200).
    """
    url = f"{BASE_URL}/update_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200, "Password update failed."


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log
