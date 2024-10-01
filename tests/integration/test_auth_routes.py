#!/usr/bin/env python3
"""
Module for integration testing
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


class TestAuthRoutes(BaseTestCase):
    """
    Test all the authentication routes
    """

    def test_register_user_success(self) -> None:
        """
        Test register user route
        """
        self.assertEqual(self.resp.status_code, 201)
        self.assertEqual(
            self.resp.get_json().get('status'), 'success'
        )

    def test_register_user_validation_error(self) -> None:
        """
        Test register user route with invalid details
        """
        error = {
            'status': 'fail',
            'data': [
                {'name': 'name is required'},
                {'email': 'email is required'}
            ]
        }

        resp = self.test_client.post(
            self.url + '/auth/register',
            json={
                'name': '',
                'email': '',
                'password': self.test_pwd
            }
        )

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(resp.get_json(), error)

    def test_register_user_used_email(self) -> None:
        """
        Test register user route for already used email
        """
        error = {
            'status': 'fail',
            'data': {
                'error': f"User {self.test_email} already exists"
            }
        }

        resp = self.test_client.post(
            self.url + '/auth/register',
            json=self.details
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json(), error)

    def test_register_user_invalid_details(self) -> None:
        """
        Test the register user route with invalid details
        """
        resp = self.test_client.post(
            self.url + '/auth/register',
            json={
                'name': self.test_name,
                'email': ''
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn('wrong format:', resp.get_json()['data']['error'])

    def test_login_success(self):
        """
        Test the method that logs the user in
        """
        resp = self.test_client.post(
            self.url + '/auth/login',
            json=self.login
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn('access_token', resp.get_json().get('data'))

    def test_login_validation_error(self):
        """
        Test the method that logs the user in using an invalid email
        """
        error = {
            'status': 'fail',
            'data': [
                {'email': 'email is required'},
            ]
        }

        resp = self.test_client.post(
            self.url + '/auth/login',
            json={
                'email': '',
                'password': self.test_pwd
            }
        )

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(resp.get_json(), error)

    def test_login_incorrect_password(self) -> None:
        """
        Test login method with incorrect password
        """
        error = {
            'status': 'fail',
            'data': {
                'error': 'password is incorrect'
            }
        }

        resp = self.test_client.post(
            self.url + '/auth/login',
            json={
                'email': self.test_email,
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json(), error)

    def test_login_unregistered_email(self) -> None:
        """
        Test login method with unregistered email
        """
        error = {
            'status': 'fail',
            'data': {
                'error': 'email not registered'
            }
        }

        resp = self.test_client.post(
            self.url + '/auth/login',
            json={
                'email': 'unregistered_email',
                'password': self.test_pwd
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json(), error)

    def test_login_invalid_details(self) -> None:
        """
        Test login method with invalid details
        """
        resp = self.test_client.post(
            self.url + '/auth/login',
            json={
                'password': self.test_pwd
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertIn('wrong format:', resp.get_json()['data']['error'])

    def test_logout(self) -> None:
        """
        Test the log out route
        """
        resp = self.test_client.get(self.url + '/auth/logout')

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.get_json(), {
            'status': 'fail',
            'data': {'token': 'missing access token'},
        })

        resp = self.test_client.post(
            self.url + '/auth/login',
            json=self.login
        )

        resp_data = resp.get_json()
        access_token = resp_data['data']['access_token']
        headers = {
            'Authorization': f"Bearer {access_token}"
        }

        resp = self.test_client.get(self.url + '/auth/logout', headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {
            'status': 'success',
            'data': {}
        })

        resp = self.test_client.get(self.url + '/auth/logout', headers=headers)

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.get_json(), {
            'status': 'fail',
            'data': {'token': 'token has been revoked'}
        })


if __name__ == '__main__':
    unittest.main()
