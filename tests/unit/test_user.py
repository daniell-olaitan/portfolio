#!/usr/bin/env python3
"""
Module for user testing
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
from models.user import User
from parameterized import parameterized

fields = [
    {
        'name': '',
        'email': 'test@test.com',
        'password': None,
        'k': 'v'
    },
    {
        'name': 'daniel olaitan',
        'email': 'daniell.olaitan@gmail.com',
        'password': 'password',
        'k': 'value'
    },
    {
        'name': '',
        'email': '',
        'password': None,
        'k': None
    }
]


class TestUser(unittest.TestCase):
    """
    Unit tests for User model
    """

    @parameterized.expand([
        ('some fail', fields[0], [
            {'name': 'name is required'},
            {'password': 'password is required'}
        ]),
        ('all pass', fields[1], []),
        ('all fail', fields[2], [
            {'name': 'name is required'},
            {'email': 'email is required'},
            {'password': 'password is required'},
            {'k': 'k is required'}
        ])
    ])
    def test_validate_user_details(
        self,
        _,
        kwargs: t.Mapping[str, t.Any],
        expected: t.List
    ) -> None:
        """
        Test the method that validates user details
        """
        errors = User.validate_user_details(**kwargs)

        self.assertEqual(expected, errors)


if __name__ == '__main__':
    unittest.main()
