import unittest
from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):

    def test_hello_world(self):
        """Тест: 'Hello, World!' -> 'hello-world'"""
        result = slugify("Hello, World!")
        self.assertEqual(result, "hello-world")

    def test_multiple_spaces(self):
        """Тест: '  multiple   spaces  ' -> 'multiple-spaces'"""
        result = slugify("  multiple   spaces  ")
        self.assertEqual(result, "multiple-spaces")

    def test_already_slug_format(self):
        """Тест: 'Already_Slug' -> 'already-slug'"""
        result = slugify("Already_Slug")
        self.assertEqual(result, "already-slug")

    def test_hyphens_collapsing(self):
        """Тест: '---A---B---' -> 'a-b'"""
        result = slugify("---A---B---")
        self.assertEqual(result, "a-b")

    def test_special_characters_only(self):
        """Тест: '!!!' -> ''"""
        result = slugify("!!!")
        self.assertEqual(result, "")

    def test_empty_string(self):
        """Тест: пустая строка -> пустая строка"""
        result = slugify("")
        self.assertEqual(result, "")

    def test_mixed_case_and_underscores(self):
        """Тест: 'Test_Case Example' -> 'test-case-example'"""
        result = slugify("Test_Case Example")
        self.assertEqual(result, "test-case-example")

    def test_numbers_and_letters(self):
        """Тест: 'Test123 ABC' -> 'test123-abc'"""
        result = slugify("Test123 ABC")
        self.assertEqual(result, "test123-abc")

    def test_leading_trailing_hyphens_removed(self):
        """Тест: '-test-string-' -> 'test-string'"""
        result = slugify("-test-string-")
        self.assertEqual(result, "test-string")

    def test_single_letter(self):
        """Тест: 'A' -> 'a'"""
        result = slugify("A")
        self.assertEqual(result, "a")


if __name__ == '__main__':
    unittest.main()