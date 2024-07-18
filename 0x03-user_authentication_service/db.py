#!/usr/bin/env python3
"""DataBase

Raises:
    InvalidRequestError
    NoResultFound
    ValueError

Returns
"""


import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """constructor method
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ _session property

        Returns:
            Session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add_user method

        Args:
            email (str)
            hashed_password (str): hashed password

        Returns:
            User
        """

        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        method to find user
        
        Return:
            user
        """

        if not kwargs:
            raise InvalidRequestError

        columns_users = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in columns_users:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            return NoResultFound

        return user

    def update_user(self, user_id, **kwargs) -> None:
        """
        method that update the user
        """

        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError('User with id {} not found'.format(user_id))

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError('User has no attribute {}'.format(key))
            setattr(user, key, value)

        try:
            self.__session.commit()
        except InvalidRequestError:
            raise ValueError('Invalid Request')
