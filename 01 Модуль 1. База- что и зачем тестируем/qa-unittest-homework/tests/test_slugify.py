import unittest
from qautils.slugify import slugify

class TestSlugify(unittest.TestCase):
    
    def test_hello_world(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")
    
    def test_multiple_spaces(self):
        self.assertEqual(slugify("  multiple   spaces  "), "multiple-spaces")
    
    def test_already_slug_with_underscore(self):
        self.assertEqual(slugify("Already_Slug"), "already-slug")
    
    def test_dashes_around_letters(self):
        self.assertEqual(slugify("---A---B---"), "a-b")
    
    def test_only_punctuation(self):
        self.assertEqual(slugify("!!!"), "")
    
    def test_empty_string(self):
        self.assertEqual(slugify(""), "")
    
    def test_mixed_underscores_and_spaces(self):
        self.assertEqual(slugify("  hello _ world  _  "), "hello-world")
    
    def test_with_numbers(self):
        self.assertEqual(slugify("Python 3.10"), "python-3-10")

if __name__ == "__main__":
    unittest.main()