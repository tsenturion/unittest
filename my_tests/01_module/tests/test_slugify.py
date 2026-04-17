import unittest

from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):

    def test_basic_phrase(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_multiple_spaces(self):
        self.assertEqual(slugify("  multiple   spaces  "), "multiple-spaces")

    def test_underscore(self):
        self.assertEqual(slugify("Already_Slug"), "already-slug")


if __name__ == "__main__":
    unittest.main()