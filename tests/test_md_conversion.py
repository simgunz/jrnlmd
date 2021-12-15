import datetime
import tempfile
import unittest

import pytest
from jrnlmd.jrnlmd import (
    add_note_to_dict,
    parse_date,
    parse_input,
    dict_to_md,
    md_to_dict,
    parse_note,
    split_list_on_delimiter,
)


def write_md_file(text):
    f = tempfile.mktemp()
    open(f, "w").write(text)


class TestMdToDictConversion(unittest.TestCase):
    def test_md_to_dict_one_level(self):
        text = """
# 2021-01-01
## topic1

- first line
- second line
"""
        d = md_to_dict(text)
        self.assertEqual({"2021-01-01": {"topic1": "- first line\n- second line\n"}}, d)

    def test_md_to_dict_two_topics(self):
        text = """
# 2021-01-01
## topic1

- first line
- second line

## topic2

- third line
"""
        d = md_to_dict(text)
        self.assertEqual(
            {
                "2021-01-01": {
                    "topic1": "- first line\n- second line\n",
                    "topic2": "- third line\n",
                }
            },
            d,
        )

    def test_md_to_dict_wrapped_lines(self):
        text = """
# 2021-01-01
## topic1

- first line
  wrapped
- second line
  ```bash
  sudo pacman -S bash
  ```
"""
        d = md_to_dict(text)
        self.assertEqual(
            {
                "2021-01-01": {
                    "topic1": "- first line\n  wrapped\n- second line\n  ```bash\n  sudo pacman -S bash\n  ```\n"
                }
            },
            d,
        )

    def test_md_to_dict_malformed_journal(self):
        text = """
## topic1

- first line
- second line
"""
        with pytest.raises(ValueError):
            md_to_dict(text)

    def test_md_to_dict_comment_in_code_fence(self):
        text = """
# 2021-01-01
## topic1

- first line
  wrapped
- second line
  ```bash
  # comment
  sudo pacman -S bash
  ```
"""
        d = md_to_dict(text)
        self.assertEqual(
            {
                "2021-01-01": {
                    "topic1": "- first line\n  wrapped\n- second line\n  ```bash\n  # comment\n  sudo pacman -S bash\n  ```\n"
                }
            },
            d,
        )


class TestDictToMdConversion(unittest.TestCase):
    def test_dict_to_md_one_level(self):
        d = {"2021-01-01": {"topic1": "- first line\n- second line\n"}}
        text = dict_to_md(d)
        self.assertEqual(
            """# 2021-01-01

## topic1

- first line
- second line
""",
            text,
        )

    def test_dict_to_md_comment_in_code_fence(self):
        d = {
            "2021-01-01": {
                "topic1": "- first line\n  wrapped\n- second line\n  ```bash\n  # comment\n  sudo pacman -S bash\n  ```\n"
            }
        }
        text = dict_to_md(d)
        self.assertEqual(
            """# 2021-01-01

## topic1

- first line
  wrapped
- second line
  ```bash
  # comment
  sudo pacman -S bash
  ```
""",
            text,
        )

    def test_dict_to_md_two_levels(self):
        d = {
            "2021-01-01": {"topic1": "- first line\n- second line\n"},
            "2021-01-02": {
                "topic2": "- third line\n",
                "topic3": "- fourth line\n- fifth line\n",
            },
        }
        text = dict_to_md(d)
        self.assertEqual(
            """# 2021-01-01

## topic1

- first line
- second line

# 2021-01-02

## topic2

- third line

## topic3

- fourth line
- fifth line
""",
            text,
        )


class TestAddNoteToDict(unittest.TestCase):
    def setUp(self):
        self.d = {
            "2021-01-01": {"topic1": "- first line\n- second line\n"},
            "2021-01-02": {
                "topic2": "- third line\n",
                "topic3": "- fourth line\n- fifth line\n",
            },
        }

    def test_add_note_to_dict(self):
        new_topic = "topic1"
        new_date = "2021-01-01"
        new_note = "- my note"
        updated_d = add_note_to_dict(self.d, new_note, new_date, new_topic)
        self.assertEqual(
            {
                "2021-01-01": {"topic1": "- first line\n- second line\n- my note\n"},
                "2021-01-02": {
                    "topic2": "- third line\n",
                    "topic3": "- fourth line\n- fifth line\n",
                },
            },
            updated_d,
        )

    def test_add_note_without_dash_to_dict(self):
        new_topic = "topic1"
        new_date = "2021-01-01"
        new_note = "my note"
        updated_d = add_note_to_dict(self.d, new_note, new_date, new_topic)
        self.assertEqual(
            {
                "2021-01-01": {"topic1": "- first line\n- second line\n- my note\n"},
                "2021-01-02": {
                    "topic2": "- third line\n",
                    "topic3": "- fourth line\n- fifth line\n",
                },
            },
            updated_d,
        )


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


class TestDateParser(unittest.TestCase):
    def test_date_parser(self):
        txt_date = "12nov2021"
        iso_date = parse_date(txt_date)
        self.assertEqual("2021-11-12", iso_date)

    def test_date_parser_unparsable(self):
        txt_date = "aaaa"
        iso_date = parse_date(txt_date)
        self.assertEqual(None, iso_date)

    def test_date_parser_single_char(self):
        txt_date = "a"
        iso_date = parse_date(txt_date)
        self.assertEqual(None, iso_date)


class TestInputParser(unittest.TestCase):
    def setUp(self):
        date_today = datetime.date.today()
        self.today = date_today.strftime("%Y-%m-%d")

    def test_input_single_note(self):
        txt_input = "a note"
        date, topic, note = parse_input(txt_input)
        self.assertEqual(self.today, date)
        self.assertEqual("ungrouped", topic)
        self.assertEqual("a note", note)

    def test_input_single_note_with_date(self):
        txt_input = "12nov2021 a note"
        date, topic, note = parse_input(txt_input)
        self.assertEqual("2021-11-12", date)
        self.assertEqual("ungrouped", topic)
        self.assertEqual("a note", note)

    def test_input_single_note_with_topic(self):
        txt_input = "topic1 is this . a note"
        date, topic, note = parse_input(txt_input)
        self.assertEqual(self.today, date)
        self.assertEqual("topic1 is this", topic)
        self.assertEqual("a note", note)


class TestSplitListOnDelimiter(unittest.TestCase):
    def test_split_with_no_delimiter(self):
        tokens = ["word1", "word2", "word3"]
        result = split_list_on_delimiter(tokens, delimiter=".")
        self.assertEqual((["word1", "word2", "word3"],), result)

    def test_split_with_one_delimiter(self):
        tokens = ["word1", ".", "word2", "word3"]
        result = split_list_on_delimiter(tokens, delimiter=".")
        self.assertEqual((["word1"], ["word2", "word3"]), result)
