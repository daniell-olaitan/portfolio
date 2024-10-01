#!/usr/bin/env python3
"""
Module for test base class
"""
import unittest
from app import create_app
from models import db


class BaseTestCase(unittest.TestCase):
    """
    Class for Base Test case that test cases can inherit from
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up default values before the test
        """
        cls.app = create_app('testing')
        cls.db = db
        cls.app_context = cls.app.app_context()
        cls.test_client = cls.app.test_client()
        cls.test_name = 'testname'
        cls.test_email = 'testemail@email.com'
        cls.test_pwd = 'testpwd'
        cls.url = '/v1'
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
        self.db.create_all()
        self.resp = self.test_client.post(
            self.url + '/auth/register',
            json=self.details
        )

    def tearDown(self) -> None:
        """
        Remove the app context and the database
        """
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()
