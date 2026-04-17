# tests/test_math_utils.py
# Модуль 1
import unittest

from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):
    def test_register(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_spaces(self):
        self.assertEqual(slugify("  multiple   spaces  "), "multiple-spaces")

    def test_slug(self):
        self.assertEqual(slugify("Already_Slug"), "already-slug")

    def test_tire(self):
        self.assertEqual(slugify("---A---B---"), "a-b")

    def test_punckt(self):
        self.assertEqual(slugify("!!!"), "")

    def test_punckt2(self):
        self.assertEqual(slugify("!  +)#$+Hello?   ,-Wor ld!!"), "hello-wor-ld")


if __name__ == "__main__":
    unittest.main()