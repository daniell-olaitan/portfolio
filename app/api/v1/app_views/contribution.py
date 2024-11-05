#!/usr/bin/env python3
"""
Module for views related to open source contribution resource
"""
from models.user import User
from utils import APINamespace
from app.api.v1.app_views import app_views
from models.contribution import Contribution
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required

contribution = APINamespace(Contribution)


@app_views.route('/users/<string:user_id>/contributions', methods=['POST'])
@jwt_required()
@contribution.verify_resource_ownership(User, 'user_id', 'id')
@contribution.validate_json_input()
def create_contribution(user_id: str) -> ResponseReturnValue:
    """
    Create a new contribution for a user
    """
    return contribution.create_resource(
        [{
            'id': user_id,
            'name': 'user_id',
            'type': User
        }]
    )


@app_views.route('/contributions/<string:contribution_id>', methods=['GET'])
def read_contribution(contribution_id: str) -> ResponseReturnValue:
    """
    Fetch a contribution
    """
    return contribution.get_resource(contribution_id)


@app_views.route('/users/<string:user_id>/contributions', methods=['GET'])
def read_contributions(user_id: str) -> ResponseReturnValue:
    """
    Fetch all the contributions of a user
    """
    return contribution.get_resources_from_relationship(User, user_id, 'contributions')


@app_views.route('/contributions/<string:contribution_id>', methods=['PATCH'])
@jwt_required()
@contribution.verify_resource_ownership(Contribution, 'contribution_id', 'user_id')
@contribution.validate_json_input()
def update_contribution(contribution_id: str) -> ResponseReturnValue:
    """
    Update a user's contribution
    """
    return contribution.update_resource(contribution_id)


@app_views.route('/contributions/<string:contribution_id>', methods=['DELETE'])
@jwt_required()
@contribution.verify_resource_ownership(Contribution, 'contribution_id', 'user_id')
def delete_contribution(contribution_id: str) -> ResponseReturnValue:
    """
    Update a user's contribution
    """
    return contribution.delete_resource(contribution_id)
