#!/usr/bin/env python3
"""
Module for authentication
"""
from os import getenv
from models import db
from hashlib import md5
from datetime import (
    datetime,
    timedelta
)
from models.user import User
import typing as t
from flask import (
    jsonify,
    current_app
)
from app import (
    jwt,
    mail
)
from flask_mail import Message
from models.invalid_token import InvalidToken
from flask.typing import ResponseReturnValue
from itsdangerous import URLSafeTimedSerializer

ModelType = t.TypeVar('Model')


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(
    jwt_header: t.Mapping[str, str],
    jwt_payload: t.Mapping[str, str]
) -> bool:
    """
    Check if user has logged out
    """
    jti = jwt_payload['jti']
    return InvalidToken.verify_jti(jti)


@jwt.expired_token_loader
def expired_token_callback(
    jwt_header: t.Mapping[str, str],
    jwt_payload: t.Mapping[str, str]
) -> ResponseReturnValue:
    """
    Check if access_token has expired
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'token has expired'},
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(
    jwt_header: t.Mapping[str, str],
    jwt_payload: t.Mapping[str, str]
) -> ResponseReturnValue:
    """
    Check if access_token has been revoked
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'token has been revoked'},
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(_) -> ResponseReturnValue:
    """
    Handle unauthorized access
    """
    return jsonify({
        'status': 'fail',
        'data': {'token': 'missing access token'},
    }), 401


class Auth:
    """
    Class for user authentication
    """
    def authenticate_user(self, email: str, password: str) -> ModelType:
        """
        Validate user login details
        """
        user = db.fetch_object(User, email=email)
        if user:
            hashed_password = md5(password.encode('utf-8'))
            if user.password == hashed_password.hexdigest():
                return user

            return None

        raise ValueError('email not registered')

    def generate_otp(self) -> str:
        import random

        return str(random.randint(100000, 999999))

    def save_otp(self, key: str, otp: str) -> None:
        from storage import redis_client

        redis_client.setex(key, 300, otp)

    def verify_otp(self, key: str, otp: str) -> bool:
        from storage import redis_client

        saved_otp = redis_client.get(key)
        redis_client.delete(key)
        if not saved_otp:
            return False

        if saved_otp != otp:
            return False

        return True
