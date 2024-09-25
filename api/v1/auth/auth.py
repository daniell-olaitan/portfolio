#!/usr/bin/env python3
"""
Module for authentication
"""
from models import db
from hashlib import md5
from models.user import User
import typing as t

ModelType = t.TypeVar('Model')


class Auth:
    """
    Class for user authentication
    """

    def authenticate_user(self, email: str, password: str) -> ModelType:
        """
        Validate user login details
        """
        user = db.fetch_object_by(User, email=email)
        if user:
            hashed_password = md5(password.encode('utf-8'))
            if user[0].password == hashed_password.hexdigest():
                return user[0]

            return None

        raise ValueError('email not registered')

    def register_user(
        self,
        name: str,
        email: str,
        password: str
    ) -> ModelType:
        """
        Create and save a new user
        """
        user = db.fetch_object_by(User, email=email)
        if user:
            raise ValueError(f"User {email} already exists")

        user = db.add_object(User, name=name, email=email, password=password)
        return user
