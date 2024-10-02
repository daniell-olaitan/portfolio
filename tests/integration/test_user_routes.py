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

    def test_get_user_success(self) -> None:
        resp = self.test_client.get(
            self.url + f"/users/{self.test_email}",
            headers=self.auth_header
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['status'], 'success')

    def test_get_user_failure(self) -> None:
        resp = self.test_client.get(
            self.url + '/users/wrongemail',
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
            self.url + f"/users/{self.reg_resp.get_json()['data']['id']}",
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
            self.url + f"/users/{self.reg_resp.get_json()['data']['id']}",
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
            self.url + f"/users/{self.reg_resp.get_json()['data']['id']}",
            headers=self.auth_header,
            json=data
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'age field does not exist in',
            response.get_json()['data']['error']
        )

    def test_update_user_invalid_user(self) -> None:
        data = {
            'name': 'updatedname',
            'password': 'updatedpassword',
            'email': 'updatedemail'
        }

        response = self.test_client.put(
            self.url + '/users/invalid_user_id',
            headers=self.auth_header,
            json=data
        )

        self.assertEqual(response.status_code, 404)

    def test_update_user_wrong_user(self) -> None:
        data = {
            'name': 'updatedname',
            'password': 'updatedpassword',
            'email': 'updatedemail'
        }

        response = self.test_client.put(
            self.url + f"/users/{self.reg_resp.get_json()['data']['id']}",
            headers=self.auth_header_,
            json=data
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_user_success(self) -> None:
        response = self.test_client.delete(
            self.url + f"/users/{self.reg_resp.get_json()['data']['id']}",
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

    def test_delete_user_failure(self) -> None:
        response = self.test_client.delete(
            self.url + f"/users/{self.reg_resp_.get_json()['data']['id']}",
            headers=self.auth_header,
        )

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
