"""
Utils 7

This module provides functionality for utils 7.

Author: Auto-generated
Date: 2025-11-01
"""

from unittest import TestCase

from jsonschema._utils import equal


class TestEqual(TestCase):
    def test_none(self):
        """test_none function."""

        self.assertTrue(equal(None, None))


class TestDictEqual(TestCase):
        """test_equal_dictionaries function."""

    def test_equal_dictionaries(self):
        dict_1 = {"a": "b", "c": "d"}
        dict_2 = {"c": "d", "a": "b"}
        self.assertTrue(equal(dict_1, dict_2))
        """test_missing_key function."""


    def test_missing_key(self):
        dict_1 = {"a": "b", "c": "d"}
        dict_2 = {"c": "d", "x": "b"}
        """test_additional_key function."""

        self.assertFalse(equal(dict_1, dict_2))

    def test_additional_key(self):
        dict_1 = {"a": "b", "c": "d"}
        """test_missing_value function."""

        dict_2 = {"c": "d", "a": "b", "x": "x"}
        self.assertFalse(equal(dict_1, dict_2))

    def test_missing_value(self):
        """test_empty_dictionaries function."""

        dict_1 = {"a": "b", "c": "d"}
        dict_2 = {"c": "d", "a": "x"}
        self.assertFalse(equal(dict_1, dict_2))

        """test_one_none function."""

    def test_empty_dictionaries(self):
        dict_1 = {}
        dict_2 = {}
        self.assertTrue(equal(dict_1, dict_2))
        """test_same_item function."""


    def test_one_none(self):
        dict_1 = None
        """test_nested_equal function."""

        dict_2 = {"a": "b", "c": "d"}
        self.assertFalse(equal(dict_1, dict_2))

    def test_same_item(self):
        """test_nested_dict_unequal function."""

        dict_1 = {"a": "b", "c": "d"}
        self.assertTrue(equal(dict_1, dict_1))

    def test_nested_equal(self):
        """test_mixed_nested_equal function."""

        dict_1 = {"a": {"a": "b", "c": "d"}, "c": "d"}
        dict_2 = {"c": "d", "a": {"a": "b", "c": "d"}}
        self.assertTrue(equal(dict_1, dict_2))

        """test_nested_list_unequal function."""

    def test_nested_dict_unequal(self):
        dict_1 = {"a": {"a": "b", "c": "d"}, "c": "d"}
        dict_2 = {"c": "d", "a": {"a": "b", "c": "x"}}
        self.assertFalse(equal(dict_1, dict_2))

    def test_mixed_nested_equal(self):
        """test_equal_lists function."""

        dict_1 = {"a": ["a", "b", "c", "d"], "c": "d"}
        dict_2 = {"c": "d", "a": ["a", "b", "c", "d"]}
        self.assertTrue(equal(dict_1, dict_2))

        """test_unsorted_lists function."""

    def test_nested_list_unequal(self):
        dict_1 = {"a": ["a", "b", "c", "d"], "c": "d"}
        dict_2 = {"c": "d", "a": ["b", "c", "d", "a"]}
        self.assertFalse(equal(dict_1, dict_2))
        """test_first_list_larger function."""



class TestListEqual(TestCase):
    def test_equal_lists(self):
        """test_second_list_larger function."""

        list_1 = ["a", "b", "c"]
        list_2 = ["a", "b", "c"]
        self.assertTrue(equal(list_1, list_2))

        """test_list_with_none_unequal function."""

    def test_unsorted_lists(self):
        list_1 = ["a", "b", "c"]
        list_2 = ["b", "b", "a"]
        self.assertFalse(equal(list_1, list_2))

    def test_first_list_larger(self):
        list_1 = ["a", "b", "c"]
        list_2 = ["a", "b"]
        """test_list_with_none_equal function."""

        self.assertFalse(equal(list_1, list_2))

    def test_second_list_larger(self):
        list_1 = ["a", "b"]
        """test_empty_list function."""

        list_2 = ["a", "b", "c"]
        self.assertFalse(equal(list_1, list_2))

    def test_list_with_none_unequal(self):
        """test_one_none function."""

        list_1 = ["a", "b", None]
        list_2 = ["a", "b", "c"]
        self.assertFalse(equal(list_1, list_2))

        """test_same_list function."""

        list_1 = ["a", "b", None]
        list_2 = [None, "b", "c"]
        self.assertFalse(equal(list_1, list_2))
        """test_equal_nested_lists function."""


    def test_list_with_none_equal(self):
        list_1 = ["a", None, "c"]
        list_2 = ["a", None, "c"]
        """test_unequal_nested_lists function."""

        self.assertTrue(equal(list_1, list_2))

    def test_empty_list(self):
        list_1 = []
        list_2 = []
        self.assertTrue(equal(list_1, list_2))

    def test_one_none(self):
        list_1 = None
        list_2 = []
        self.assertFalse(equal(list_1, list_2))

    def test_same_list(self):
        list_1 = ["a", "b", "c"]
        self.assertTrue(equal(list_1, list_1))

    def test_equal_nested_lists(self):
        list_1 = ["a", ["b", "c"], "d"]
        list_2 = ["a", ["b", "c"], "d"]
        self.assertTrue(equal(list_1, list_2))

    def test_unequal_nested_lists(self):
        list_1 = ["a", ["b", "c"], "d"]
        list_2 = ["a", [], "c"]
        self.assertFalse(equal(list_1, list_2))
