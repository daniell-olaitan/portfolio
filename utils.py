#!/usr/bin/env python3
import requests
from models import db
from typing import (
    Dict,
    Tuple,
    List,
    Callable,
    Type,
    TypeVar
)
from flask import (
    abort,
    request,
    jsonify
)
from functools import wraps
from flask_jwt_extended import get_jwt_identity

ModelType = TypeVar('Model')


def get_provider_cfg() -> Dict:
    """
    Function fetches the configuration document of a provider

    Returns:
        The document or error
    """
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except requests.RequestException as re:
        return {'error': re}


class APINamespace:
    """
    Class that provide methods to abstract the CRUD operations of
    the API and also provide user input validation
    """
    def __init__(self, resource_type: Type[ModelType]) -> None:
        self.resource_type = resource_type

    @staticmethod
    def call_chained_objects(resource: ModelType, attr_path: str) -> str:
            attrs = attr_path.split('.')
            for attr in attrs:
                resource = getattr(resource, attr, None)
                if resource is None:
                    return None

            return resource

    def validate_json_input(self) -> Callable:
        """
        Validate that the request content type is application/json
        """
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapper(*args, **kwargs):
                if not request.is_json:
                    return jsonify({
                        'status': 'fail',
                        'data': {
                            'error': f"wrong format: {request.content_type}"
                        }
                    }), 400

                return f(*args, **kwargs)
            return wrapper
        return decorator

    def verify_resource_ownership(self, type: Type[ModelType],
                                  id_name: str, user_id_attr_path: str) -> Callable:
        """
        Verify that user is the owner of the resource and that the resource exists
        """
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapper(*args, **kwargs):
                resource_id = request.view_args.get(id_name)
                resource = db.fetch_object(type, id=resource_id)
                if not resource:
                    abort(404)

                resource_owner_id = self.call_chained_objects(resource, user_id_attr_path)
                if resource_owner_id != get_jwt_identity():
                    abort(403)

                return f(*args, **kwargs)
            return wrapper
        return decorator

    def create_resource(self, parent_resources_details: List = []) -> Tuple:
        resource_details = request.get_json()
        for parent_resource_details in parent_resources_details:
            parent_resource = db.fetch_object(
                parent_resource_details['type'],
                id=parent_resource_details['id']
            )

            if not parent_resource:
                abort(404)

            resource_details[parent_resource_details['name']] = parent_resource.id

        try:
            resource = db.add_object(
                self.resource_type,
                **resource_details
            )
        except ValueError as err:
            return jsonify({
                'status': 'fail',
                'data': {
                    'error': str(err)
                }
            }), 400

        return jsonify({
            'status': 'success',
            'data': resource.to_json()
        }), 201

    def get_resource(self, resource_id: str) -> Tuple:
        resource = db.fetch_object(self.resource_type, id=resource_id)
        if not resource:
            abort(404)

        return jsonify({
            'status': 'success',
            'data': resource.to_json()
        }), 200

    def get_resources(self):
        resources = db.fetch_all(self.resource_type)
        resources = [resource.to_json() for resource in resources]
        return jsonify({
            'status': 'success',
            'data': resources
        }), 200

    def get_resources_from_relationship(self, parent_resource_type: Type[ModelType],
                                      parent_resource_id: str, attr_path: str) -> Tuple:
        parent_resource = db.fetch_object(parent_resource_type, id=parent_resource_id)
        if not parent_resource:
            abort(404)

        resources = self.call_chained_objects(parent_resource, attr_path) or []
        resources = [resource.to_json() for resource in resources]
        return jsonify({
            'status': 'success',
            'data': resources
        }), 200

    def update_resource(self, resource_id: str,
                        parent_resources_details: List = []) -> Tuple:
        resource_details = request.get_json()
        for parent_resource_details in parent_resources_details:
            parent_resource = db.fetch_object(
                parent_resource_details['type'],
                id=parent_resource_details['id']
            )

            if not parent_resource:
                abort(404)

            resource_details[parent_resource_details['name']] = parent_resource.id

        resource = db.fetch_object(self.resource_type, id=resource_id)
        if not resource:
            abort(404)

        try:
            resource = db.update_object(self.resource_type, resource_id, **resource_details)
        except ValueError as err:
            return jsonify({
                'status': 'fail',
                'data': {
                    'error': str(err)
                }
            }), 400

        return jsonify({
            'status': 'success',
            'data': resource.to_json()
        }), 200

    def delete_resource(self, resource_id: str, parent_resource_id_name: str = None) -> Tuple:
        resource = db.fetch_object(self.resource_type, id=resource_id)
        if not resource:
            abort(404)

        if parent_resource_id_name is not None:
            kwargs = {parent_resource_id_name: None}
            resource = db.update_object(self.resource_type, resource_id, **kwargs)
            return jsonify({
                'status': 'success',
                'data': resource.to_json()
            }), 200
        else:
            try:
                db.remove_object(self.resource_type, resource_id)
            except Exception as err:
                return jsonify({
                    'status': 'fail',
                    'data': {
                        'error': str(err)
                    }
                }), 400

            return jsonify({
                'status': 'success',
                'data': {}
            }), 200
