#!/usr/bin/env python3
"""
    function that return the log message obfuscated
"""

import re
from typing import List
import logging
import os
from dataclasses import field
import mysql.connector
from ast import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            function that return logger msg with format
        """
        message = super(RedactingFormatter, self).format(record)
        log_record = filter_datum(self.fields, self.REDACTION,
                                  message, self.SEPARATOR)
        return log_record


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
        function that make obfuscate on message
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


def get_logger() -> logging.Logger:
    """
    function that return a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        return database connection
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    psw = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    host = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(user=user,
                                         password=psw,
                                         host=host,
                                         database=db_name)
    return connection


def main() -> None:
    """
    entry point
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

