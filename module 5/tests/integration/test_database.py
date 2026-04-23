import unittest
import os
from mypkg.calculator import save_to_db

class TestDatabase(unittest.TestCase):
    def test_save_number(self):
        result = save_to_db(42)
        self.assertEqual(result, "Saved 42 to database")
    
    def test_save_string_raises(self):
        with self.assertRaises(ValueError):
            save_to_db("not a number")
    
    @unittest.skipUnless(os.getenv("SLOW_TESTS") == "1", "Slow test disabled")
    def test_bulk_save(self):
        for i in range(1000):
            save_to_db(i)
        self.assertTrue(True)
