#!/usr/bin/env python3
"""
Module for views related to profile resource
"""
from models.user import User
from app.api.v1.app_views import app_views
from flask.typing import ResponseReturnValue
from models.user_profile import UserProfile
from utils import APINamespace
from flask_jwt_extended import jwt_required

profile = APINamespace(UserProfile)


@app_views.route('users/<string:user_id>/profiles', methods=['POST'])
@jwt_required()
@profile.verify_resource_ownership(User, 'user_id', 'id')
@profile.validate_json_input()
def create_profile(user_id: str) -> ResponseReturnValue:
    """
    Create a profile for a user
    """
    return profile.create_resource(
        [{
            'id': user_id,
            'name': 'user_id',
            'type': User
        }]
    )


@app_views.route('/profiles/<string:profile_id>', methods=['PATCH'])
@jwt_required()
@profile.verify_resource_ownership(UserProfile, 'profile_id', 'user_id')
@profile.validate_json_input()
def update_profile(profile_id: str) -> ResponseReturnValue:
    """
    Update a user's profile
    """
    return profile.update_resource(profile_id)


@app_views.route('/profiles/<string:profile_id>', methods=['DELETE'])
@jwt_required()
@profile.verify_resource_ownership(UserProfile, 'profile_id', 'user_id')
def delete_profile(profile_id: str) -> ResponseReturnValue:
    """
    Delete a user's profile
    """
    return profile.delete_resource(profile_id)


@app_views.route('/profiles/<string:profile_id>', methods=['GET'])
def read_profile(profile_id: str) -> ResponseReturnValue:
    """
    Get a user's profile
    """
    return profile.get_resource(profile_id)
