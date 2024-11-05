#!/usr/bin/env python3
"""
Module for views related to contact resource
"""
from app.api.v1.app_views import app_views
from models.contact import Contact
from models.user_profile import UserProfile
from flask.typing import ResponseReturnValue
from flask_jwt_extended import jwt_required
from utils import APINamespace

contact = APINamespace(Contact)


@app_views.route('profiles/<string:profile_id>/contacts', methods=['POST'])
@jwt_required()
@contact.verify_resource_ownership(UserProfile, 'profile_id', 'user_id')
@contact.validate_json_input()
def create_contact(profile_id: str) -> ResponseReturnValue:
    """
    Create a contact for a profile
    """
    return contact.create_resource(
        [{
            'id': profile_id,
            'name': 'user_profile_id',
            'type': UserProfile
        }]
    )


@app_views.route('/contacts/<string:contact_id>', methods=['PATCH'])
@jwt_required()
@contact.verify_resource_ownership(Contact, 'contact_id', 'user_profile.user_id')
@contact.validate_json_input()
def update_contact(contact_id: str) -> ResponseReturnValue:
    """
    Update a user's contact
    """
    return contact.update_resource(contact_id)


@app_views.route('/contacts/<string:contact_id>', methods=['GET'])
def read_contact(contact_id: str) -> ResponseReturnValue:
    """
    Fetch a contact
    """
    return contact.get_resource(contact_id)


@app_views.route('/profiles/<string:profile_id>/contacts', methods=['GET'])
def read_contacts(profile_id: str) -> ResponseReturnValue:
    """
    Fetch all the contacts of a profile
    """
    return contact.get_resources_from_relationship(UserProfile, profile_id, 'contacts')


@app_views.route('/contacts/<string:contact_id>', methods=['DELETE'])
@jwt_required()
@contact.verify_resource_ownership(Contact, 'contact_id', 'user_profile.user_id')
def delete_contact(contact_id: str) -> ResponseReturnValue:
    """
    Delete a user contact
    """
    return contact.delete_resource(contact_id)
