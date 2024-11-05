#!/usr/bin/env python3
"""
Module for views related to open source feature resource
"""
from utils import APINamespace
from models.project import Project
from app.api.v1.app_views import app_views
from models.feature import Feature
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required

feature = APINamespace(Feature)


@app_views.route('/projects/<string:project_id>/features', methods=['POST'])
@jwt_required()
@feature.verify_resource_ownership(Project, 'project_id', 'user_id')
@feature.validate_json_input()
def create_feature(project_id: str) -> ResponseReturnValue:
    """
    Create a new feature for a project
    """
    return feature.create_resource(
        [{
            'id': project_id,
            'name': 'project_id',
            'type': Project
        }]
    )


@app_views.route('/features/<string:feature_id>', methods=['GET'])
def read_feature(feature_id: str) -> ResponseReturnValue:
    """
    Fetch a feature
    """
    return feature.get_resource(feature_id)


@app_views.route('/projects/<string:project_id>/features', methods=['GET'])
def read_features(project_id: str) -> ResponseReturnValue:
    """
    Fetch all the features of a project
    """
    return feature.get_resources_from_relationship(
        Project,
        project_id,
        'features'
    )


@app_views.route('/features/<string:feature_id>', methods=['PATCH'])
@jwt_required()
@feature.verify_resource_ownership(Feature, 'feature_id', 'project.user_id')
@feature.validate_json_input()
def update_feature(feature_id: str) -> ResponseReturnValue:
    """
    Update a project's feature
    """
    return feature.update_resource(feature_id)


@app_views.route('/features/<string:feature_id>', methods=['DELETE'])
@jwt_required()
@feature.verify_resource_ownership(Feature, 'feature_id', 'project.user_id')
def delete_feature(feature_id: str) -> ResponseReturnValue:
    """
    Update a project's feature
    """
    return feature.delete_resource(feature_id)
