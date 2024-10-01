#!/usr/bin/env python3
"""
Module for user routes integration testing
"""
import os
import sys

# This will allow this test file to be run from the current directory
# using python3 <test_file.py> or <./test_file.py>
current_directory = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_directory, "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import unittest
from tests.integration.base_test import BaseTestCase
from models.user import User


class TestUserRoutes(BaseTestCase):
    """
    Class to test all the routes in user views
    """

    def setUp(self) -> None:
        super().setUp()
        self.login_resp = self.test_client.post(
            self.url + '/auth/login',
            json=self.login
        )

        self.access_token = self.login_resp.get_json()['data']['access_token']
        self.auth_header = {
            'Authorization': f"Bearer {self.access_token}"
        }

    def test_get_user_success(self) -> None:
        resp = self.test_client.get(
            self.url + '/users/me',
            headers=self.auth_header
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['status'], 'success')

    def test_get_user_failure(self) -> None:
        id = self.resp.get_json()['data']['id']
        user = self.db.fetch_an_object_by(User, id=id)
        self.db.remove_object(user)

        resp = self.test_client.get(
            self.url + '/users/me',
            headers=self.auth_header
        )

        self.assertEqual(resp.status_code, 404)

    def test_update_user_success(self) -> None:
        data = {
            'name': 'updatedname',
            'password': 'updatedpassword',
            'email': 'updatedemail'
        }

        response = self.test_client.put(
            self.url + f"/users/{self.resp.get_json()['data']['id']}",
            headers=self.auth_header,
            json=data
        )

        details = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(details['data']['name'], 'updatedname')
        self.assertEqual(details['data']['email'], 'updatedemail')

    def test_update_user_wrong_input_format(self) -> None:
        data = {
            'name': 'updated_name',
            'password': 'updatedpassword',
            'email': 'updatedemail'
        }

        response = self.test_client.put(
            self.url + f"/users/{self.resp.get_json()['data']['id']}",
            headers=self.auth_header,
            data=data
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'wrong format',
            response.get_json()['data']['error']
        )

    def test_update_user_wrong_field(self) -> None:
        data = {
            'name': 'updated_name',
            'age': 'updatedage',
            'email': 'updatedemail'
        }

        response = self.test_client.put(
            self.url + f"/users/{self.resp.get_json()['data']['id']}",
            headers=self.auth_header,
            json=data
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'age field does not exist in',
            response.get_json()['data']['error']
        )

    def test_delete_user(self) -> None:
        response = self.test_client.delete(
            self.url + f"/users/{self.resp.get_json()['data']['id']}",
            headers=self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

        response = self.test_client.post(
            self.url + '/auth/login',
            json=self.login
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {
            'status': 'fail',
            'data': {
                'error': 'email not registered'
            }
        })
