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
import typing as t
from parameterized import parameterized
from models import db
from api import create_app


class TestAuthRoutes(unittest.TestCase):
    """
    Test all the routes in the application
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up default values before the test
        """
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.test_client = cls.app.test_client()
        cls.test_name = 'testname'
        cls.test_email = 'testemail@email.com'
        cls.test_pwd = 'testpwd'
        cls.url = '/api/v1/auth'
        cls.details = {
            'name': cls.test_name,
            'email': cls.test_email,
            'password': cls.test_pwd
        }

        cls.login = {
            'email': cls.test_email,
            'password': cls.test_pwd
        }

    def setUp(self) -> None:
        """
        Set the app context and create the database
        """
        self.app_context.push()
        db.create_all()
        self.resp = self.test_client.post(
            self.url + '/register',
            json=self.details
        )

    def tearDown(self) -> None:
        """
        Remove the app context and the database
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
            self.url + '/register',
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
                'email': f"User {self.test_email} already exists"
            }
        }

        resp = self.test_client.post(
            self.url + '/register',
            json=self.details
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json(), error)

    def test_register_user_invalid_details(self) -> None:
        """
        Test the register user route with invalid details
        """
        error = {
            'status': 'fail',
            'data': {
                'user_details': 'invalid user details'
            }
        }

        resp = self.test_client.post(
            self.url + '/register',
            json={
                'name': self.test_name,
                'email': ''
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json(), error)

    def test_login_success(self):
        """
        Test the method that logs the user in
        """
        resp = self.test_client.post(
            self.url + '/login',
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
            self.url + '/login',
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
                'password': 'password is incorrect'
            }
        }

        resp = self.test_client.post(
            self.url + '/login',
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
                'email': 'email not registered'
            }
        }

        resp = self.test_client.post(
            self.url + '/login',
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
        error = {
            'status': 'fail',
            'data': {
                'user_details': 'invalid user details'
            }
        }

        resp = self.test_client.post(
            self.url + '/login',
            json={
                'password': self.test_pwd
            }
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json(), error)

    def test_logout(self) -> None:
        """
        Test the log out route
        """
        resp = self.test_client.get(self.url + '/logout')

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.get_json(), {
            'status': 'fail',
            'data': {'token': 'missing access token'},
        })

        resp = self.test_client.post(
            self.url + '/login',
            json=self.login
        )

        resp_data = resp.get_json()
        access_token = resp_data['data']['access_token']
        headers = {
            'Authorization': f"Bearer {access_token}"
        }

        resp = self.test_client.get(self.url + '/logout', headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {
            'status': 'success',
            'data': None
        })

        resp = self.test_client.get(self.url + '/logout', headers=headers)

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.get_json(), {
            'status': 'fail',
            'data': {'token': 'token has been revoked'}
        })


if __name__ == '__main__':
    unittest.main()
