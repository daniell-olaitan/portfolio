#!/usr/bin/env python3
"""
Module for testing database storge Class
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
from unittest.mock import (
    patch,
    MagicMock
)
from models.engines.db_storage import DBStorage
import uuid


class TestDBStrorage(unittest.TestCase):
    """
    Test class for DBStorage class
    """

    @patch('models.engines.db_storage.SQLAlchemy')
    def setUp(self, _) -> None:
        """
        Set up default values before the test
        """
        self.db = DBStorage()
        self.mock_session = MagicMock()
        self.db.session = self.mock_session

    def test_add_object_success(self):
        """
        Test the save method
        """
        mock_table = MagicMock()
        mock_table.columns.keys.return_value = ['test1', 'test2']
        mock_class = MagicMock(__table__=mock_table)
        mock_obj = MagicMock()
        mock_class.return_value = mock_obj
        mock_kwargs = {'test1': 'test', 'test2': 12}

        obj = self.db.add_object(mock_class, **mock_kwargs)

        self.assertEqual(obj, mock_obj)
        mock_class.assert_called_once_with(**mock_kwargs)
        self.mock_session.add.assert_called_once_with(mock_obj)
        self.mock_session.commit.assert_called_once()

    def test_add_object_failure(self):
        """
        Test the save method with wrong field
        """
        mock_table = MagicMock()
        mock_table.columns.keys.return_value = ['test1', 'test2']
        mock_class = MagicMock(__table__=mock_table, __name__='Test')
        mock_obj = MagicMock()
        mock_class.return_value = mock_obj
        mock_kwargs = {'test1': 'test', 'test3': 12}

        with self.assertRaises(ValueError) as ctx:
            _ = self.db.add_object(mock_class, **mock_kwargs)

        self.mock_session.add.assert_not_called()
        self.mock_session.commit.assert_not_called()
        self.mock_session.rollback.assert_not_called()
        self.assertEqual(
            str(ctx.exception),
            f"test3 field does not exist in Test Model"
        )

    def test_remove_object(self):
        """
        Test the remove method
        """
        mock_obj = MagicMock()

        self.db.remove_object(mock_obj)

        self.mock_session.delete.assert_called_once_with(mock_obj)
        self.mock_session.commit.assert_called_once()
        self.mock_session.roolback.assert_not_called()

    def test_fetch_an_object_by(self):
        """
        Test the fetch_obj_by method
        """
        mock_class = MagicMock()
        mock_obj = MagicMock()
        mock_kwargs = {'name': 'test', 'value': 12}
        mock_query = self.mock_session.query.return_value
        mock_filter = mock_query.filter_by.return_value
        mock_filter.first.return_value = mock_obj


        obj = self.db.fetch_an_object_by(mock_class, **mock_kwargs)

        self.mock_session.query.assert_called_once_with(mock_class)
        mock_query.filter_by.assert_called_once_with(
            **mock_kwargs
        )

        self.assertEqual(obj, mock_obj)

    def test_fetch_object_by(self):
        """
        Test the fetch_obj_by method
        """
        mock_class = MagicMock()
        mock_objs = MagicMock()
        mock_kwargs = {'name': 'test', 'value': 12}
        mock_query = self.mock_session.query.return_value
        mock_filter = mock_query.filter_by.return_value
        mock_filter.all.return_value = mock_objs


        objs = self.db.fetch_object_by(mock_class, **mock_kwargs)

        self.mock_session.query.assert_called_once_with(mock_class)
        mock_query.filter_by.assert_called_once_with(
            **mock_kwargs
        )

        self.assertEqual(objs, mock_objs)

    def test_update_object_valid_key(self):
        """
        Test the update_object method with valid keys
        """
        mock_id = str(uuid.uuid4())
        mock_class = MagicMock()
        mock_kwargs = {'name': 'test', 'value': 12}
        mock_obj = MagicMock(id=mock_id)
        mock_table = MagicMock()
        mock_table.columns.keys.return_value = ['name', 'value']
        mock_obj.__table__ = mock_table
        self.mock_session.get.return_value = mock_obj

        self.db.update_object(mock_class, mock_id, **mock_kwargs)

        self.mock_session.get.assert_called_with(mock_class, mock_id)

        for key, value in mock_kwargs.items():
            self.assertEqual(getattr(mock_obj, key), value)

        self.mock_session.add.assert_called_once_with(mock_obj)
        self.mock_session.commit.assert_called_once()

    def test_update_object_invalid_key(self):
        """
        Test the update_object method with invalid keys
        """
        mock_id = str(uuid.uuid4())
        mock_class = MagicMock(__name__='Test')
        mock_kwargs = {'age': 12}
        mock_obj = MagicMock(id=mock_id)
        mock_table = MagicMock()
        mock_table.columns.keys.return_value = ['name', 'value']
        mock_obj.__table__ = mock_table
        self.mock_session.get.return_value = mock_obj

        with self.assertRaises(ValueError) as ctx:
            self.db.update_object(mock_class, mock_id, **mock_kwargs)

        self.mock_session.get.assert_called_once_with(mock_class, mock_id)
        self.mock_session.add.assert_not_called()
        self.mock_session.commit.assert_not_called()
        self.mock_session.rollback.assert_not_called()
        self.assertEqual(
            str(ctx.exception),
            f"age field does not exist in Test Model"
        )


if __name__ == '__main__':
    unittest.main()
