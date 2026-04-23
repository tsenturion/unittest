import unittest
from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):
    
    def test_basic_conversion(self):
        """Тест базового преобразования"""
        self.assertEqual(slugify("Hello, World!"), "hello-world")
    
    def test_multiple_spaces(self):
        """Тест множественных пробелов"""
        self.assertEqual(slugify("  multiple   spaces  "), "multiple-spaces")
    
    def test_underscores_to_dashes(self):
        """Тест замены подчёркиваний на дефисы"""
        self.assertEqual(slugify("Already_Slug"), "already-slug")
    
    def test_collapse_dashes(self):
        """Тест схлопывания подряд идущих дефисов"""
        self.assertEqual(slugify("---A---B---"), "a-b")
    
    def test_only_invalid_chars(self):
        """Тест строки только из недопустимых символов"""
        self.assertEqual(slugify("!!!"), "")
    
    def test_mixed_separators(self):
        """Тест смеси пробелов и подчёркиваний"""
        self.assertEqual(slugify("Hello _ world"), "hello-world")
    
    def test_preserve_digits(self):
        """Тест сохранения цифр"""
        self.assertEqual(slugify("Version 2.0"), "version-20")
    
    def test_empty_string(self):
        """Тест пустой строки"""
        self.assertEqual(slugify(""), "")
    
    def test_tabs_and_newlines(self):
        """Тест с табами и переводами строк"""
        self.assertEqual(slugify("one\ttwo\nthree"), "one-two-three")
    
    def test_leading_trailing_dashes(self):
        """Тест обрезания дефисов в начале и конце"""
        self.assertEqual(slugify("-hello-world-"), "hello-world")


if __name__ == "__main__":
    unittest.main()
