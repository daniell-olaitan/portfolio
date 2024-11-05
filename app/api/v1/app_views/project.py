#!/usr/bin/env python3
"""
Module for views related to project resource
"""
from models import db
from flask import jsonify
from models.user import User
from app.api.v1.app_views import app_views
from utils import APINamespace
from models.project import Project
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required

project = APINamespace(Project)
errors = {
    '404': {
        'status': 'fail',
        'data': {
            'error': 'not found'
        }
    },
    '403': {
        'status': 'fail',
        'data': {
            'error': 'you are forbidden to perform this action'
        }
    }
}


@app_views.route('/users/<string:user_id>/projects', methods=['POST'])
@jwt_required()
@project.verify_resource_ownership(User, 'user_id', 'id')
@project.validate_json_input()
def create_project(user_id: str) -> ResponseReturnValue:
    """
    Create a new project for a user
    """
    return project.create_resource(
        [{
            'id': user_id,
            'name': 'user_id',
            'type': User
        }]
    )


@app_views.route('/projects/<string:project_id>', methods=['GET'])
def read_project(project_id: str) -> ResponseReturnValue:
    """
    Fetch a project
    """
    return project.get_resource(project_id)


@app_views.route('/users/<string:user_id>/projects', methods=['GET'])
def read_projects(user_id: str) -> ResponseReturnValue:
    """
    Fetch all the projects of a user
    """
    return project.get_resources_from_relationship(User, user_id, 'projects')


@app_views.route('/projects/<string:project_id>', methods=['PATCH'])
@jwt_required()
@project.verify_resource_ownership(Project, 'project_id', 'user_id')
@project.validate_json_input()
def update_project(project_id: str) -> ResponseReturnValue:
    """
    Update a user's project
    """
    return project.update_resource(project_id)


@app_views.route('/projects/<string:project_id>', methods=['DELETE'])
@jwt_required()
@project.verify_resource_ownership(Project, 'project_id', 'user_id')
def delete_project(project_id: str) -> ResponseReturnValue:
    """
    Update a user's project
    """
    return project.delete_resource(project_id)
