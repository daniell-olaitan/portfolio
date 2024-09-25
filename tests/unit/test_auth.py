#!/usr/bin/env python3
"""
Module to test Auth class
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
from hashlib import md5
from api.v1.auth.auth import Auth
from unittest.mock import (
    patch,
    MagicMock
)


class TestAuth(unittest.TestCase):
    """
    Class to test the Auth methods
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_name = 'testname'
        cls.test_password = 'testpassword'
        cls.test_email = 'testemail@email.com'
        cls.auth = Auth()
        password = md5(cls.test_password.encode('utf-8')).hexdigest()
        cls.mock_user = MagicMock(email=cls.test_email, password=password)

    @patch('models.db.fetch_object_by')
    def test_authenticate_user_success(self, mock_fetch: MagicMock) -> None:
        """
        Test the method that authenticate user for valid input
        """
        mock_fetch.return_value = self.mock_user

        user = self.auth.authenticate_user(self.test_email, self.test_password)

        self.assertEqual(user, self.mock_user)

    @patch('models.db.fetch_object_by')
    def test_authenticate_user_incorrect_password(
        self,
        mock_fetch: MagicMock
    ) -> None:
        """
        Test the method that authenticate user for incorrect pwd
        """
        mock_fetch.return_value = self.mock_user
        wrong_password = 'wrong_password'

        user = self.auth.authenticate_user(self.test_email, wrong_password)

        self.assertIsNone(user)

    @patch('models.db.fetch_object_by')
    def test_authenticate_user_unregistered_email(
        self,
        mock_fetch: MagicMock
    ) -> None:
        """
        Test the method that authenticate user for unregistered email
        """
        mock_fetch.return_value = None

        with self.assertRaises(ValueError) as ctx:
            _ = self.auth.authenticate_user(
                self.test_email, self.test_password
            )

        self.assertEqual(str(ctx.exception), 'email not registered')

    @patch('models.db.fetch_object_by')
    @patch('models.db.add_object')
    def test_register_user_success(
        self,
        mock_add: MagicMock,
        mock_fetch: MagicMock
    ) -> None:
        """
        Test the Auth method that creates and register new user
        """
        mock_fetch.return_value = None
        mock_add.return_value = self.mock_user

        user = self.auth.register_user(
            self.test_name,
            self.test_email,
            self.test_password
        )

        self.assertEqual(user, self.mock_user)

    @patch('models.db.fetch_object_by')
    @patch('models.db.add_object')
    def test_register_user_registered_email(
        self,
        mock_add: MagicMock,
        mock_fetch: MagicMock
    ) -> None:
        """
        Test the Auth method that creates and register new user
        """
        mock_fetch.return_value = self.mock_user
        mock_add.return_value = None

        with self.assertRaises(ValueError) as ctx:
            user = self.auth.register_user(
                self.test_name,
                self.test_email,
                self.test_password
            )

        self.assertEqual(
            str(ctx.exception),
            f"User {self.test_email} already exists"
        )

        mock_add.assert_not_called()


if __name__ == '__main__':
    unittest.main()
