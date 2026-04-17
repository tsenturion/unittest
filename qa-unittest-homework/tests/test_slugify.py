import unittest
import sys
import os

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# ПРАВИЛЬНЫЙ ИМПОРТ - импортируем функцию, а не модуль
from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):
    """Test cases for slugify function."""
    
    def test_lowercase_conversion(self):
        """Test that string is converted to lowercase."""
        self.assertEqual(slugify("HELLO WORLD"), "hello-world")
        self.assertEqual(slugify("Hello World"), "hello-world")
    
    def test_space_replacement(self):
        """Test that spaces are replaced with hyphens."""
        self.assertEqual(slugify("hello world"), "hello-world")
        self.assertEqual(slugify("a b c"), "a-b-c")
        self.assertEqual(slugify("multiple   spaces"), "multiple-spaces")
    
    def test_underscore_replacement(self):
        """Test that underscores are replaced with hyphens."""
        self.assertEqual(slugify("hello_world"), "hello-world")
        self.assertEqual(slugify("_hello_"), "hello")
        self.assertEqual(slugify("a_b_c"), "a-b-c")
    
    def test_special_chars_removal(self):
        """Test that special characters are removed."""
        self.assertEqual(slugify("Hello, World!"), "hello-world")
        # Исправлено: точка удаляется, а не заменяется на дефис
        self.assertEqual(slugify("email@example.com"), "emailexamplecom")  # было "emailexample-com"
        self.assertEqual(slugify("Price: $100"), "price-100")
        self.assertEqual(slugify("Hello!!!???***"), "hello")
    
    def test_numbers_preserved(self):
        """Test that numbers are preserved."""
        self.assertEqual(slugify("item123"), "item123")
        self.assertEqual(slugify("version 2.0"), "version-20")
        self.assertEqual(slugify("file_2024_01_15"), "file-2024-01-15")
    
    def test_consecutive_dashes_collapsing(self):
        """Test that multiple consecutive dashes are collapsed."""
        self.assertEqual(slugify("a---b---c"), "a-b-c")
        self.assertEqual(slugify("hello----world"), "hello-world")
        self.assertEqual(slugify("---A---B---"), "a-b")
    
    def test_trim_leading_trailing_dashes(self):
        """Test that leading and trailing dashes are removed."""
        self.assertEqual(slugify("-hello-world-"), "hello-world")
        self.assertEqual(slugify("---hello---"), "hello")
        self.assertEqual(slugify("-a-b-c-"), "a-b-c")
    
    def test_empty_string(self):
        """Test that empty string returns empty string."""
        self.assertEqual(slugify(""), "")
    
    def test_string_with_no_valid_chars(self):
        """Test that string with no valid chars returns empty string."""
        self.assertEqual(slugify("!!!"), "")
        self.assertEqual(slugify("   "), "")
        self.assertEqual(slugify("_-_-_"), "")
    
    def test_multiple_spaces(self):
        """Test multiple spaces are handled correctly."""
        self.assertEqual(slugify("  multiple   spaces  "), "multiple-spaces")
    
    def test_mixed_spaces_and_underscores(self):
        """Test combination of spaces and underscores."""
        self.assertEqual(slugify("hello_world test"), "hello-world-test")
        self.assertEqual(slugify("_hello world_"), "hello-world")
    
    def test_specification_examples(self):
        """Test the exact examples from the specification."""
        self.assertEqual(slugify("Hello, World!"), "hello-world")
        self.assertEqual(slugify("  multiple   spaces  "), "multiple-spaces")
        self.assertEqual(slugify("Already_Slug"), "already-slug")
        self.assertEqual(slugify("---A---B---"), "a-b")
        self.assertEqual(slugify("!!!"), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)