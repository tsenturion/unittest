import unittest
from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):
    
    def test_lowercase_conversion(self):
        self.assertEqual(slugify("HELLO World"), "hello-world")
        self.assertEqual(slugify("Python Is Great"), "python-is-great")
        self.assertEqual(slugify("UPPERCASE"), "uppercase")
    
    def test_replace_spaces_and_underscores(self):
        self.assertEqual(slugify("hello world"), "hello-world")
        self.assertEqual(slugify("hello_world"), "hello-world")
        self.assertEqual(slugify("hello world and_python"), "hello-world-and-python")
        self.assertEqual(slugify("_test_ test"), "test-test")
    
    def test_remove_invalid_characters(self):
        self.assertEqual(slugify("hello@world!"), "helloworld")
        self.assertEqual(slugify("привет мир"), "")
        self.assertEqual(slugify("test123!@#$%^&*()"), "test123")
        self.assertEqual(slugify("hello-world!!!"), "hello-world")
        self.assertEqual(slugify("café"), "caf")
        self.assertEqual(slugify("русский english"), "english")
    
    def test_collapse_multiple_dashes(self):
        self.assertEqual(slugify("hello--world"), "hello-world")
        self.assertEqual(slugify("hello---world"), "hello-world")
        self.assertEqual(slugify("hello - world"), "hello-world")
        self.assertEqual(slugify("hello  -  world"), "hello-world")
    
    def test_trim_dashes_at_ends(self):
        self.assertEqual(slugify("-hello-world-"), "hello-world")
        self.assertEqual(slugify("--hello--world--"), "hello-world")
        self.assertEqual(slugify("-hello-"), "hello")
        self.assertEqual(slugify("hello-"), "hello")
        self.assertEqual(slugify("-hello"), "hello")
    
    def test_empty_string_returns_empty(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify(None), "")
    
    def test_string_that_becomes_empty_returns_empty(self):
        self.assertEqual(slugify("!!!@@@###"), "")
        self.assertEqual(slugify("привет мир"), "")
        self.assertEqual(slugify("---"), "")
        self.assertEqual(slugify("_"), "")
        self.assertEqual(slugify(" "), "")
        self.assertEqual(slugify("_-_"), "")
    
    
    def test_digits_preserved(self):
        self.assertEqual(slugify("test123"), "test123")
        self.assertEqual(slugify("123 456"), "123-456")
    
    def test_only_valid_characters(self):
        self.assertEqual(slugify("abc-123"), "abc-123")
        self.assertEqual(slugify("a-b-c-1-2-3"), "a-b-c-1-2-3")


if __name__ == '__main__':
    unittest.main()