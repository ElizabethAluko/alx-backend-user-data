#!/usr/bin/env python3
"""Module contains functions to encrypt password using bcrypt package"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string.

    arg:
        password: To be hashed.

    Return:
        hashed password.
    """
    password = password.encode('utf-8')
    return (bcrypt.hashpw(password, bcrypt.gensalt()))
