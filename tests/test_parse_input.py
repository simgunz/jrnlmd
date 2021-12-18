import unittest
import datetime

from jrnlmd.jrnlmd import parse_input


class TestInputParser(unittest.TestCase):
    def setUp(self):
        date_today = datetime.date.today()
        self.today = date_today.strftime("%Y-%m-%d")

    def test_input_single_note(self):
        txt_input = "a note"
        date, topic, note = parse_input(txt_input)
        self.assertEqual(self.today, date)
        self.assertEqual("ungrouped", topic)
        self.assertEqual("- a note\n", note)

    def test_input_single_note_with_date(self):
        txt_input = "12nov2021 a note"
        date, topic, note = parse_input(txt_input)
        self.assertEqual("2021-11-12", date)
        self.assertEqual("ungrouped", topic)
        self.assertEqual("- a note\n", note)

    def test_input_single_note_with_topic(self):
        txt_input = "topic1 is this . a note"
        date, topic, note = parse_input(txt_input)
        self.assertEqual(self.today, date)
        self.assertEqual("topic1 is this", topic)
        self.assertEqual("- a note\n", note)

    def test_input_single_note_with_date_and_topic(self):
        txt_input = "12nov2021 topic1 is this . a note"
        date, topic, note = parse_input(txt_input)
        self.assertEqual("2021-11-12", date)
        self.assertEqual("topic1 is this", topic)
        self.assertEqual("- a note\n", note)

    def test_input_multiple_notes_with_date_and_topic(self):
        txt_input = (
            "12nov2021 topic1 is this . first bullet , second bullet , third bullet"
        )
        date, topic, note = parse_input(txt_input)
        self.assertEqual("2021-11-12", date)
        self.assertEqual("topic1 is this", topic)
        self.assertEqual("- first bullet\n- second bullet\n- third bullet\n", note)
