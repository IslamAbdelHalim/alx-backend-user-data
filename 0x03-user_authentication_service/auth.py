#!/usr/bin/env python3
"""
creating a hash password
"""

import bcrypt


def _hash_password(password: str) -> str:
    """
    function creating hash password

    Args:
        password str
    Return:
        hashed password
    """

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password
