#!/usr/bin/env python3
"""The module contains tasks on how to handle personal data"""

import os
import mysql.connector
import re
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "password", "ssn")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filters specified fields in a message and replaces their
    values with redaction.

    Args:
        fields (List[str]): List of field names to be filtered.
        redaction (str): The value to replace filtered fields with.
        message (str): The log message to filter.
        separator (str): The character used to separate fields
        in the log message.

    Returns:
        str: The filtered log message.
    """
    for field in fields:
        pattern = f'{field}=[^{separator}]+'
        replacement = f'{field}={redaction}'
        message = re.sub(pattern, replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes a RedactingFormatter instance.

        Args:
            fields (list[str]): List of field names to be
            redacted in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats log records and filters specified fields using
        filter_datum function.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with redacted fields.
        """
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Get the logger of a given user_data"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(
            PII_FIELDS,
            "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database using environment
    variables.

    Returns:
        Optional[mysql.connector.connection.MySQLConnection]:
        A database connection or None if the connection fails.
    """
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connection
