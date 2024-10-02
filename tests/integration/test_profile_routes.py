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
from models.user_profile import UserProfile


class TestProfile(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.profile_data = {
            'image_url': 'testimageurl',
            'bio': 'testbio',
            'location': 'testlocation',
            'project_header': 'testprojectheader',
            'work_header': 'testworkheader',
            'article_header': 'testarticleheader',
            'resume': 'testresume'
        }

        self.updated_data = {
            'image_url': 'updatedimageurl',
            'bio': 'updatedbio',
            'location': 'updatedlocation',
            'project_header': 'updatedprojectheader',
            'work_header': 'updatedworkheader',
            'article_header': 'updatedarticleheader',
            'resume': 'updatedresume'
        }

        self.prof_resp = self.test_client.post(
            self.url + f"/users/{self.reg_resp.get_json()['data']['id']}/profiles",
            json=self.profile_data,
            headers=self.auth_header
        )

    def test_create_profile_success(self):
        self.assertEqual(self.prof_resp.status_code, 201)
        self.assertEqual(self.prof_resp.get_json()['status'], 'success')

    def test_create_profile_wrong_user(self):
        response = self.test_client.post(
            self.url + f"/users/{self.reg_resp_.get_json()['data']['id']}/profiles",
            json=self.profile_data,
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 404)

    def test_create_user_invalid_user(self):
        response = self.test_client.post(
            self.url + '/users/invalid_user/profiles',
            json=self.profile_data,
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 404)

    def test_create_user_wrong_field(self):
        self.profile_data['test3'] = 'test3'
        response = self.test_client.post(
            self.url + f"/users/{self.reg_resp.get_json()['data']['id']}/profiles",
            json=self.profile_data,
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            f"test3 field does not exist in",
            response.get_json()['data']['error']
        )

    def test_create_user_wrong_input_format(self):
        response = self.test_client.post(
            self.url + f"/users/{self.reg_resp_.get_json()['data']['id']}/profiles",
            data=self.profile_data,
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'wrong format',
            response.get_json()['data']['error']
        )

    def test_update_profile_success(self):
        response = self.test_client.put(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header,
            json=self.updated_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_update_profile_wrong_user(self):
        response = self.test_client.put(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header_,
            json=self.updated_data
        )

        self.assertEqual(response.status_code, 404)

    def test_update_profile_invalid_profile(self):
        response = self.test_client.put(
            self.url + '/profiles/invalid_profile',
            headers=self.auth_header,
            json=self.updated_data
        )

        self.assertEqual(response.status_code, 404)

    def test_update_profile_wrong_format(self):
        response = self.test_client.put(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header,
            data=self.updated_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'wrong format',
            response.get_json()['data']['error']
        )

    def test_update_profile_invalid_field(self):
        self.updated_data['test3'] = 'test3'
        response = self.test_client.put(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header,
            json=self.updated_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            f"test3 field does not exist in",
            response.get_json()['data']['error']
        )

    def test_delete_profile_success(self):
        response = self.test_client.delete(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

        response = self.test_client.get(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 404)

    def delete_profile_wrong_user(self):
        response = self.test_client.delete(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header_
        )

        self.assertEqual(response.status_code, 404)

    def delete_profile_invalid_profile(self):
        response = self.test_client.delete(
            self.url + '/profiles/invalid_profile',
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 404)

    def test_get_profile_success(self):
        response = self.test_client.get(
            self.url + f"/profiles/{self.prof_resp.get_json()['data']['id']}",
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_get_profile_invalid_profile(self):
        response = self.test_client.get(
            self.url + '/profiles/invalid_profile',
            headers=self.auth_header
        )

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
