#!/usr/bin/env python3
"""Module contains functions to encrypt password using bcrypt package"""
import bcrypt


def hash_password(password):
    """Returns a salted, hashed password, which is a byte string.

    arg:
        password: To be hashed.

    Return:
        hashed password.
    """
    return (bcrypt.hashpw(password, bcrypt.gensalt()))
