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
        cls.test_email = 'testemail'
        cls.test_pwd = 'testpassword'
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

        cls.test_name_ = 'testname2'
        cls.test_email_ = 'testemail2'
        cls.test_pwd_ = 'testpassword2'
        cls.details_ = {
            'name': cls.test_name_,
            'email': cls.test_email_,
            'password': cls.test_pwd_
        }

        cls.login_ = {
            'email': cls.test_email_,
            'password': cls.test_pwd_
        }

    def setUp(self) -> None:
        """
        Set the app context and create the database
        """
        self.app_context.push()
        self.db.create_all()
        self.reg_resp = self.test_client.post(
            self.url + '/auth/register',
            json=self.details
        )

        self.reg_resp_ = self.test_client.post(
            self.url + '/auth/register',
            json=self.details_
        )

        self.login_resp = self.test_client.post(
            self.url + '/auth/login',
            json=self.login
        )

        self.login_resp_ = self.test_client.post(
            self.url + '/auth/login',
            json=self.login_
        )

        self.access_token = self.login_resp.get_json()['data']['access_token']
        self.auth_header = {
            'Authorization': f"Bearer {self.access_token}"
        }

        self.access_token_ = self.login_resp_.get_json()['data']['access_token']
        self.auth_header_ = {
            'Authorization': f"Bearer {self.access_token_}"
        }

    def tearDown(self) -> None:
        """
        Remove the app context and the database
        """
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()
