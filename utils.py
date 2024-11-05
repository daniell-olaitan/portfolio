#!/usr/bin/env python3
import requests
from models import db
from typing import (
    Dict,
    Tuple,
    List,
    Callable,
    Type,
    TypeVar,
    Optional
)
from flask import (
    request,
    jsonify,
    session
)
from functools import wraps
from flask_jwt_extended import get_jwt_identity

ModelType = TypeVar('Model')
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


def login_required(f: Callable) -> Callable:
    from flask import redirect, url_for, session
    @wraps(f)
    def wrapper(*args, **kwargs) -> Callable:
        resp = requests.get(
            'http://127.0.0.1:5000/v1/users/current-user',
            headers=session.get('auth')
        )

        if resp.status_code == 401:
            return redirect(url_for('admin.login'))

        session['current_user'] = resp.json()['data']
        return f(*args, **kwargs)
    return wrapper


def encode_details(item_name: str, item: Dict) -> Dict:
    encoded_dict = {}
    resource = {}
    del item['updated_at']
    encoded_dict['item_name'] = item_name
    encoded_dict['item_id'] = item.pop('id')
    encoded_dict['heading'] = item_name[:-1].capitalize()
    encoded_dict['date'] = item.pop('created_at').split('T')[0]
    for key, value in item.items():
        if key.endswith('_id'):
            continue
        else:
            words = [word.capitalize() for word in key.split('_')]
            key = ' '.join(words)
            resource[key] = value

    encoded_dict['details'] = resource
    return encoded_dict


def delete_file(filename: str) -> None:
    import os
    from portfolio import app

    path = os.path.join(app.root_path, os.getenv('UPLOAD_DIRECTORY'), filename)
    if os.path.exists(path):
        os.remove(path)


def handle_files(details: Dict, files: Dict) -> Dict:
    """
    Handle the file upload and save
    """
    import os
    import uuid
    from portfolio import app
    from werkzeug.utils import secure_filename

    directory = os.path.join(app.root_path, os.getenv('UPLOAD_DIRECTORY'))
    os.makedirs(directory, exist_ok=True)
    if files:
        for key in files:
            file = files[key]
            if file.filename:
                filename = secure_filename(file.filename)
                filename = key + '-' + str(uuid.uuid4()) + filename
                file.save(os.path.join(directory, filename))
                details[key] = filename

    return details


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
                if ('multipart/form-data' not in request.content_type and
                        'application/x-www-form-urlencoded' not in request.content_type):
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
                    return jsonify(errors['404']), 404

                resource_owner_id = self.call_chained_objects(resource, user_id_attr_path)
                if resource_owner_id != get_jwt_identity():
                    return jsonify(errors['404']), 403

                return f(*args, **kwargs)
            return wrapper
        return decorator

    def create_resource(self, parent_resources_details: List = []) -> Tuple:
        resource_details = request.form.to_dict()
        for parent_resource_details in parent_resources_details:
            parent_resource = db.fetch_object(
                parent_resource_details['type'],
                id=parent_resource_details['id']
            )

            if not parent_resource:
                return jsonify(errors['404']), 404

            resource_details[parent_resource_details['name']] = parent_resource.id

        try:
            details = handle_files(resource_details, request.files)
            resource = db.add_object(
                self.resource_type,
                **details
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
            return jsonify(errors['404']), 404

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
            return jsonify(errors['404']), 404

        resources = self.call_chained_objects(parent_resource, attr_path) or []
        resources = [resource.to_json() for resource in resources]
        return jsonify({
            'status': 'success',
            'data': resources
        }), 200

    def update_resource(self, resource_id: str,
                        parent_resources_details: List = []) -> Tuple:
        import os
        from portfolio import app

        resource_details = request.form.to_dict()
        for parent_resource_details in parent_resources_details:
            parent_resource = db.fetch_object(
                parent_resource_details['type'],
                id=parent_resource_details['id']
            )

            if not parent_resource:
                return jsonify(errors['404']), 404

            resource_details[parent_resource_details['name']] = parent_resource.id

        resource = db.fetch_object(self.resource_type, id=resource_id)
        if not resource:
            return jsonify(errors['404']), 404

        try:
            details = handle_files(resource_details, request.files)
            for field, value in resource.to_json().items():
                for key in ['image', 'picture', 'video', 'resume']:
                    if key in field:
                        if value and details.get(field):
                            file_path = os.path.join(app.root_path,
                                os.getenv('UPLOAD_DIRECTORY'),
                                value
                            )
                            if os.path.exists(file_path):
                                os.remove(file_path)
            resource = db.update_object(self.resource_type, resource_id, **details)
        except Exception as err:
            print(err)
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
            return jsonify(errors['404']), 404

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
                print(err)
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


class APIRequest:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @property
    def get_current_user(self) -> Optional[ModelType]:
        response = requests.get(
            self.base_url + '/users/current-user',
            headers=session.get('auth')
        )

        if response.headers['Content-Type'] == 'application/json':
            return response.json()['data'], response.status_code

        return response.content, response.status_code

    def make_get_request(self, url: str) -> Tuple:
        response = requests.get(self.base_url + url)
        if response.headers['Content-Type'] == 'application/json':
            return response.json()['data'], response.status_code

        return response.content, response.status_code

    def make_post_request(self, url: str, payload: Dict, file_load: Dict) -> Tuple:
        response = requests.post(
            self.base_url + url,
            data=payload,
            files=file_load,
            headers=session.get('auth')
        )

        if response.headers['Content-Type'] == 'application/json':
            return response.json()['data'], response.status_code

        return response.content, response.status_code

    def make_patch_request(self, url: str, payload: Dict, file_load: Dict) -> Tuple:
        response = requests.patch(
            self.base_url + url,
            data=payload,
            files=file_load,
            headers=session.get('auth')
        )

        if response.headers['Content-Type'] == 'application/json':
            return response.json()['data'], response.status_code

        return response.content, response.status_code

    def make_delete_request(self, url: str) -> Tuple:
        response = requests.delete(
            self.base_url + url,
            headers=session.get('auth')
        )

        if response.headers['Content-Type'] == 'application/json':
            return response.json()['data'], response.status_code

        return response.content, response.status_code
