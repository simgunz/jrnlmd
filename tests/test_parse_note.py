import unittest

from jrnlmd.jrnlmd import parse_note


class TestParseNote(unittest.TestCase):
    def test_parse_one_line_note_no_dash(self):
        note = "a note"
        parsed_note = parse_note(note)
        self.assertEqual("- a note\n", parsed_note)

    def test_parse_one_line_note_with_dash(self):
        note = "- a note"
        parsed_note = parse_note(note)
        self.assertEqual("- a note\n", parsed_note)

    def test_multiline_note(self):
        note = "- a note\n- with two lines"
        parsed_note = parse_note(note)
        self.assertEqual("- a note\n- with two lines\n", parsed_note)

    def test_multiline_note_without_dash(self):
        note = "a note\n- with two lines"
        parsed_note = parse_note(note)
        self.assertEqual("a note\n- with two lines\n", parsed_note)
