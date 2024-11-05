#!/usr/bin/env python3
"""
Module for views related to open source experience resource
"""
from utils import APINamespace
from models.work import Work
from app.api.v1.app_views import app_views
from models.experience import Experience
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required

experience = APINamespace(Experience)


@app_views.route('/works/<string:work_id>/experiences', methods=['POST'])
@jwt_required()
@experience.verify_resource_ownership(Work, 'work_id', 'user_id')
@experience.validate_json_input()
def create_experience(work_id: str) -> ResponseReturnValue:
    """
    Create a new experience for a
    """
    return experience.create_resource(
        [{
            'id': work_id,
            'name': 'work_id',
            'type': Work
        }]
    )


@app_views.route('/experiencs/<string:experience_id>', methods=['GET'])
def read_experience(experience_id: str) -> ResponseReturnValue:
    """
    Fetch a experience
    """
    return experience.get_resource(experience_id)


@app_views.route('/works/<string:work_id>/experiences', methods=['GET'])
def read_experiences(work_id: str) -> ResponseReturnValue:
    """
    Fetch all the experiences of a work
    """
    return experience.get_resources_from_relationship(
        Work,
        work_id,
        'experiences'
    )


@app_views.route('/experiences/<string:experience_id>', methods=['PATCH'])
@jwt_required()
@experience.verify_resource_ownership(Experience, 'experience_id', 'work.user_id')
@experience.validate_json_input()
def update_experience(experience_id: str) -> ResponseReturnValue:
    """
    Update a work's experience
    """
    return experience.update_resource(experience_id)


@app_views.route('/experiences/<string:experience_id>', methods=['DELETE'])
@jwt_required()
@experience.verify_resource_ownership(Experience, 'experience_id', 'work.user_id')
def delete_experience(experience_id: str) -> ResponseReturnValue:
    """
    Delete a work's experience
    """
    return experience.delete_resource(experience_id)
