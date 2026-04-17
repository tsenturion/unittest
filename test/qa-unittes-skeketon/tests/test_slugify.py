# tests/test_slugify.py
import unittest

from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):

    def test_lowercase_conversion(self):
        self.assertEqual(slugify("Hello WORLD"), "hello-world")

    def test_replace_spaces_and_underscores_with_hyphen(self):
        self.assertEqual(slugify("hello world_test"), "hello-world-test")

    def test_remove_disallowed_characters(self):
        self.assertEqual(slugify("Hello, @World! 123"), "hello-world-123")

    def test_collapse_multiple_hyphens(self):
        self.assertEqual(slugify("a--b---c"), "a-b-c")

    def test_trim_hyphens_from_ends(self):
        self.assertEqual(slugify("-hello-world-"), "hello-world")

    def test_combination_of_rules(self):
        self.assertEqual(
            slugify("  ___Hello,,   WORLD__  !!!  "),
            "hello-world"
        )

    def test_empty_string_or_only_invalid_chars_returns_empty(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("!!!"), "")
        self.assertEqual(slugify("   _-_-_   "), "")

    def test_keep_digits_and_hyphens_inside(self):
        self.assertEqual(slugify("item 123 - version 2"), "item-123-version-2")


if __name__ == "__main__":
    unittest.main()