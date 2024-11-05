#!/usr/bin/env python3
"""
Module for views related to user resource
"""
from models import db
from models.user import User
from utils import APINamespace
from app.api.v1.app_views import app_views
from flask.typing import ResponseReturnValue
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from flask import (
    abort,
    jsonify
)

user = APINamespace(User)


@app_views.route('/api/users/<string:email>', methods=['GET'])
def read_user_with_email(email: str) -> ResponseReturnValue:
    """
    Fetch the current user
    """
    user = db.fetch_object(User, email=email)
    if not user:
        abort(404)

    profile = user.profile.to_json()
    user = user.to_json()
    user['profile'] = profile

    return jsonify({
        'status': 'success',
        'data': user
    }), 200


@app_views.route('/users/<string:user_id>', methods=['GET'])
def read_user(user_id: str) -> ResponseReturnValue:
    """
    Fetch a user
    """
    return user.get_resource(user_id)


@app_views.route('/users/current-user', methods=['GET'])
def read_current_user() -> ResponseReturnValue:
    """
    Fetch the current user
    """
    from flask_jwt_extended import verify_jwt_in_request

    verify_jwt_in_request()
    user_id = get_jwt_identity()
    user = db.fetch_object(User, id=user_id)
    if not user:
        abort(401)

    return jsonify({
        'status': 'success',
        'data': user.to_json()
    }), 200


@app_views.route('/users/<string:user_id>', methods=['PATCH'])
@jwt_required()
@user.verify_resource_ownership(User, 'user_id', 'id')
@user.validate_json_input()
def update_user(user_id: str) -> ResponseReturnValue:
    """
    Update a given user
    """
    return user.update_resource(user_id)


@app_views.route('/users/<string:user_id>', methods=['DELETE'])
@jwt_required()
@user.verify_resource_ownership(User, 'user_id', 'id')
def delete_user(user_id: str) -> ResponseReturnValue:
    """
    Delete a user
    """
    return user.delete_resource(user_id)
