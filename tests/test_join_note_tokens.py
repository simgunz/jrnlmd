import unittest

from jrnlmd.jrnlmd import join_notes_tokens


class TestJointNotes(unittest.TestCase):
    def test_join_notes_tokens(self):
        notes_tokens = [["word1"], ["word2", "word3"]]
        result = join_notes_tokens(notes_tokens)
        self.assertEqual("- word1\n- word2 word3\n", result)
