#!/usr/bin/env python3
"""
Module for views related to service resource
"""
from app.api.v1.app_views import app_views
from models.service import Service
from models.user_profile import UserProfile
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required
from utils import APINamespace

service = APINamespace(Service)


@app_views.route('profiles/<string:profile_id>/services', methods=['POST'])
@jwt_required()
@service.verify_resource_ownership(UserProfile, 'profile_id', 'user_id')
@service.validate_json_input()
def create_service(profile_id: str) -> ResponseReturnValue:
    """
    Create a service for a profile
    """
    return service.create_resource(
        [{
            'id': profile_id,
            'name': 'user_profile_id',
            'type': UserProfile
        }]
    )


@app_views.route('/services/<string:service_id>', methods=['PATCH'])
@jwt_required()
@service.verify_resource_ownership(Service, 'service_id', 'user_profile.user_id')
@service.validate_json_input()
def update_service(service_id: str) -> ResponseReturnValue:
    """
    Update a user's service
    """
    return service.update_resource(service_id)


@app_views.route('/services/<string:service_id>', methods=['GET'])
def read_service(service_id: str) -> ResponseReturnValue:
    """
    Fetch a service
    """
    return service.get_resource(service_id)


@app_views.route('/profiles/<string:profile_id>/services', methods=['GET'])
def read_services(profile_id: str) -> ResponseReturnValue:
    """
    Fetch all the services of a profile
    """
    return service.get_resources_from_relationship(UserProfile, profile_id, 'services')


@app_views.route('/services/<string:service_id>', methods=['DELETE'])
@jwt_required()
@service.verify_resource_ownership(Service, 'service_id', 'user_profile.user_id')
def delete_service(service_id: str) -> ResponseReturnValue:
    """
    Delete a user service
    """
    return service.delete_resource(service_id)
