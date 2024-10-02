#!/usr/bin/env python3
"""
Module for views related to profile resource
"""
from models import db
from app.v1.app_views import app_views
from flask.typing import ResponseReturnValue
from models.user import User
from models.user_profile import UserProfile
from flask import (
    jsonify,
    abort,
    request
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@app_views.route('users/<string:user_id>/profiles', methods=['POST'])
@jwt_required()
def create_profile(user_id: str) -> ResponseReturnValue:
    """
    Create a profile for a user
    """
    try:
        profile_details = request.get_json()
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': f"wrong format: {err}"
            }
        }), 400

    if user_id != get_jwt_identity():
        abort(404)

    user = db.fetch_an_object_by(User, id=user_id)
    if not user:
        abort(404)

    try:
        profile = db.add_object(
            UserProfile,
            user_id=user.id,
            **profile_details
        )

        return jsonify({
            'status': 'success',
            'data': profile.to_json()
        }), 201
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': str(err)
            }
        }), 400


@app_views.route('/profiles/<string:profile_id>', methods=['PUT'])
@jwt_required()
def update_profile(profile_id: str) -> ResponseReturnValue:
    """
    Update a user's profile
    """
    try:
        profile_details = request.get_json()
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': f"wrong format: {err}"
            }
        }), 400

    profile = db.fetch_an_object_by(UserProfile, id=profile_id)
    if not profile:
        abort(404)

    if profile.user_id != get_jwt_identity():
        abort(404)

    try:
        profile = db.update_object(UserProfile, profile_id, **profile_details)
        return jsonify({
            'status': 'success',
            'data': profile.to_json()
        }), 200
    except ValueError as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': str(err)
            }
        }), 400


@app_views.route('/profiles/<string:profile_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(profile_id: str) -> ResponseReturnValue:
    """
    Delete a user's profile
    """
    profile = db.fetch_an_object_by(UserProfile, id=profile_id)
    if not profile:
        abort(404)

    if profile.user_id != get_jwt_identity():
        abort(404)

    try:
        db.remove_object(profile)
        return jsonify({
            'status': 'success',
            'data': {}
        }), 200
    except ValueError as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': str(err)
            }
        }), 400


@app_views.route('/profiles/<string:profile_id>', methods=['GET'])
def get_profile(profile_id: str) -> ResponseReturnValue:
    """
    Get a user's profile
    """
    profile = db.fetch_an_object_by(UserProfile, id=profile_id)
    if not profile:
        abort(404)

    return jsonify({
        'status': 'success',
        'data': profile.to_json()
    }), 200
