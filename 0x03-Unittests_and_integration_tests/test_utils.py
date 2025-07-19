#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)


@parameterized.expand([
    ({}, ("a",)),
    ({"a": 1}, ("a", "b")),
])
def test_access_nested_map_exception(self, nested_map, path):
    with self.assertRaises(KeyError) as context:
        access_nested_map(nested_map, path)
    self.assertEqual(str(context.exception), f"'{path[len(context.exception.args[0:])[0]]}'")

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json

class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        # Configure the mock to return a response with test_payload as .json()
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


import unittest
from unittest.mock import patch
from utils import memoize

class TestMemoize(unittest.TestCase):
    """Tests for utils.memoize"""

    def test_memoize(self):
        """Test that memoize caches the result"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


