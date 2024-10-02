#!/usr/bin/env python3
"""
Module for views related to user resource
"""
from app.v1.app_views import app_views
from models import db
from models.user import User
from flask.typing import ResponseReturnValue
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from flask import (
    jsonify,
    request,
    abort
)


@app_views.route('/users/<string:email>', methods=['GET'])
def get_user(email: str) -> ResponseReturnValue:
    """
    Fetch the current user
    """
    user = db.fetch_an_object_by(User, email=email)
    if not user:
        abort(404)

    return jsonify({
        'status': 'success',
        'data': user.to_json()
    }), 200


@app_views.route('/users/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id: str) -> ResponseReturnValue:
    """
    Update a given user
    """
    try:
        user_details = request.get_json()
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': f"wrong format: {err}"
            }
        }), 400

    user = db.fetch_an_object_by(User, id=user_id)
    if not user:
        abort(404)

    if user_id != get_jwt_identity():
        abort(404)

    try:
        user = db.update_object(User, user_id, **user_details)
        return jsonify({
            'status': 'success',
            'data': user.to_json()
        }), 200
    except ValueError as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': str(err)
            }
        }), 400


@app_views.route('/users/<string:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id: str) -> ResponseReturnValue:
    """
    Delete a user
    """
    user = db.fetch_an_object_by(User, id=user_id)
    if not user:
        abort(404)

    if user_id != get_jwt_identity():
        abort(404)

    db.remove_object(user)
    return jsonify({
        'status': 'success',
        'data': {}
    }), 200
