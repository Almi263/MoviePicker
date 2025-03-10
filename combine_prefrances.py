import unittest
from keyword_validator import checkKeyword

class TestKeywordValidation(unittest.TestCase):
    def test_valid_single_word(self):
        self.assertTrue(checkKeyword("magics"))

    def test_valid_part_of_word(self):
        self.assertTrue(checkKeyword("magic"))

    def test_valid_incorrect_capitalization(self):
        self.assertTrue(checkKeyword("mAGiC"))

    def test_invalid_empty_string(self):
        self.assertFalse(checkKeyword(""))

    def test_invalid_null_string(self):
        self.assertFalse(checkKeyword(None))

    def test_invalid_dne(self):
        self.assertFalse(checkKeyword("asdf"))

    def test_edge_case_with_numerals(self):
        self.assertTrue(checkKeyword("2"))

    def test_edge_case_with_spelled_words(self):
        self.assertTrue(checkKeyword("two"))

if __name__ == '__main__':
    unittest.main()