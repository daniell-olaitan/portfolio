#!/usr/bin/env python3
"""
Module for views related to work resource
"""
from models.user import User
from app.api.v1.app_views import app_views
from utils import APINamespace
from models.work import Work
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required

work = APINamespace(Work)


@app_views.route('/users/<string:user_id>/works', methods=['POST'])
@jwt_required()
@work.verify_resource_ownership(User, 'user_id', 'id')
@work.validate_json_input()
def create_work(user_id: str) -> ResponseReturnValue:
    """
    Create a new work for a user
    """
    return work.create_resource(
        [{
            'id': user_id,
            'name': 'user_id',
            'type': User
        }]
    )


@app_views.route('/works/<string:work_id>', methods=['GET'])
def read_work(work_id: str) -> ResponseReturnValue:
    """
    Fetch a work
    """
    return work.get_resource(work_id)


@app_views.route('/users/<string:user_id>/works', methods=['GET'])
def read_works(user_id: str) -> ResponseReturnValue:
    """
    Fetch all the works of a user
    """
    return work.get_resources_from_relationship(User, user_id, 'works')


@app_views.route('/works/<string:work_id>', methods=['PATCH'])
@jwt_required()
@work.verify_resource_ownership(Work, 'work_id', 'user_id')
@work.validate_json_input()
def update_work(work_id: str) -> ResponseReturnValue:
    """
    Update a user's work
    """
    return work.update_resource(work_id)


@app_views.route('/works/<string:work_id>', methods=['DELETE'])
@jwt_required()
@work.verify_resource_ownership(Work, 'work_id', 'user_id')
def delete_work(work_id: str) -> ResponseReturnValue:
    """
    Update a user's work
    """
    return work.delete_resource(work_id)
