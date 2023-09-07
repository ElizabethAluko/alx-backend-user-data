#!/usr/bin/env python3
"""Basic Authentication Module"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Returns Basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """Returns the base64 string of the authentication header"""

        if not authorization_header or not isinstance(
                authorization_header, str):
            return None
        authorization_header = authorization_header.split()
        if len(authorization_header) != 2 or authorization_header[
                0] != "Basic":
            return None
        return authorization_header[1]
