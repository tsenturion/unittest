
import unittest
from netutils.ports import parse_port

class TestParsePort(unittest.TestCase):

    def test_type_error(self):
        for v in (None, [], {}, 3.14, True):
            with self.subTest(v=v):
                with self.assertRaises(TypeError):
                    parse_port(v)

    def test_int_valid(self):
        self.assertEqual(parse_port(1), 1)
        self.assertEqual(parse_port(65535), 65535)

    def test_int_invalid(self):
        for v in (0, -1, 65536):
            with self.subTest(v=v):
                with self.assertRaises(ValueError):
                    parse_port(v)

    def test_str_valid(self):
        self.assertEqual(parse_port("80"), 80)
        self.assertEqual(parse_port(" 22 "), 22)

    def test_str_invalid(self):
        for v in ("", "abc", "+10", "-1"):
            with self.subTest(v=v):
                with self.assertRaises(ValueError):
                    parse_port(v)