#!/usr/bin/env python3
""" Module for testing utils """
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestUtils(unittest.TestCase):
    """ Class for testing utility functions """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """ Test access_nested_map function """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
        self, nested_map, path, expected_exception
    ):
        """ Test access_nested_map function with exception """
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_requests_get):
        """ Test get_json function """
        mock_json = Mock(return_value=test_payload)
        mock_requests_get.return_value.json = mock_json

        result = get_json(test_url)
        mock_requests_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

    class TestClass:
        """ Test class for memoize function """

        def a_method(self):
            """ Sample method """
            return 42

        @memoize
        def a_property(self):
            """ Sample memoized property """
            return self.a_method()

    @patch('utils.TestClass.a_method')
    def test_memoize(self, mock_a_method):
        """ Test memoize function """
        test_instance = self.TestClass()
        result_1 = test_instance.a_property()
        result_2 = test_instance.a_property()

        mock_a_method.assert_called_once()
        self.assertEqual(result_1, 42)
        self.assertEqual(result_2, 42)
