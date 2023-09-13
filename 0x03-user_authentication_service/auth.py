#!/usr/bin/env python3
"""Password Hashing Module"""


def _hash_password(self, password: str) -> bytes:
            """Hash Password"""
            salt = bcrypt.gensalt()

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password
