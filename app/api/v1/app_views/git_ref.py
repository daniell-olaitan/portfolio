#!/usr/bin/env python3
"""
Module for views related to open source gitref resource
"""
from utils import APINamespace
from models.contribution import Contribution
from app.api.v1.app_views import app_views
from models.git_ref import GitRef
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required

gitref = APINamespace(GitRef)


@app_views.route('/contributions/<string:contribution_id>/gitrefs', methods=['POST'])
@jwt_required()
@gitref.verify_resource_ownership(Contribution, 'contribution_id', 'user_id')
@gitref.validate_json_input()
def create_gitref(contribution_id: str) -> ResponseReturnValue:
    """
    Create a new gitref for a contribution
    """
    return gitref.create_resource(
        [{
            'id': contribution_id,
            'name': 'contribution_id',
            'type': Contribution
        }]
    )


@app_views.route('/gitrefs/<string:gitref_id>', methods=['GET'])
def read_gitref(gitref_id: str) -> ResponseReturnValue:
    """
    Fetch a gitref
    """
    return gitref.get_resource(gitref_id)


@app_views.route('/contributions/<string:contribution_id>/gitrefs', methods=['GET'])
def read_gitrefs(contribution_id: str) -> ResponseReturnValue:
    """
    Fetch all the gitrefs of a contribution
    """
    return gitref.get_resources_from_relationship(
        Contribution,
        contribution_id,
        'git_refs'
    )


@app_views.route('/gitrefs/<string:gitref_id>', methods=['PATCH'])
@jwt_required()
@gitref.verify_resource_ownership(GitRef, 'gitref_id', 'contribution.user_id')
@gitref.validate_json_input()
def update_gitref(gitref_id: str) -> ResponseReturnValue:
    """
    Update a contribution's gitref
    """
    return gitref.update_resource(gitref_id)


@app_views.route('/gitrefs/<string:gitref_id>', methods=['DELETE'])
@jwt_required()
@gitref.verify_resource_ownership(GitRef, 'gitref_id', 'contribution.user_id')
def delete_gitref(gitref_id: str) -> ResponseReturnValue:
    """
    Delete a contribution's gitref
    """
    return gitref.delete_resource(gitref_id)
