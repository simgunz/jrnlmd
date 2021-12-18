import unittest

from jrnlmd.jrnlmd import split_list_on_delimiter


class TestSplitListOnDelimiter(unittest.TestCase):
    def test_split_with_no_delimiter(self):
        tokens = ["word1", "word2", "word3"]
        result = split_list_on_delimiter(tokens, delimiter=".")
        self.assertEqual((["word1", "word2", "word3"],), result)

    def test_split_with_one_delimiter(self):
        tokens = ["word1", ".", "word2", "word3"]
        result = split_list_on_delimiter(tokens, delimiter=".")
        self.assertEqual((["word1"], ["word2", "word3"]), result)
