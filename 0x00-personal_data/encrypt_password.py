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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check for password match

        args:
            hashed_password: bytes type - to be compared with the password
            password: string type - to be checked.

        return:
            True: if the password matches
            False: if the passwoed does not match
    """
    password = hash_password(password)

    if password == hash_password:
        return True
    else:
        return False
