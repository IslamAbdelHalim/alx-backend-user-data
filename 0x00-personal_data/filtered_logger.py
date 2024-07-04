#!/usr/bin/env python3
"""
    function that return the log message obfuscated
"""

import re
from typing import List
import logging


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
