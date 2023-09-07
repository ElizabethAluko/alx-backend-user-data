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


    def decode_base64_authorization_header(
            self,base64_authorization_header: str) -> str:
        """
        Decode base64 authorization authentication
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header == None or not isinstance(
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
