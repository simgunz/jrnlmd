from unittest import mock

from jrnlmd.journal_entry import UNDEFINED_TOPIC, JournalEntry


def test_journal_entry_default_constructor(today):
    entry = JournalEntry()
    assert "" == entry.note
    assert today == entry.date
    assert UNDEFINED_TOPIC == entry.topic


def test_journal_entry_constructor_note_only(today):
    note = "- a note"
    entry = JournalEntry(note)
    assert JournalEntry._parse_note(note) == entry.note
    assert today == entry.date
    assert UNDEFINED_TOPIC == entry.topic


def test_journal_entry_constructor_with_unparsed_note_only(today):
    note = "a note"
    entry = JournalEntry(note)
    assert JournalEntry._parse_note(note) == entry.note
    assert today == entry.date
    assert UNDEFINED_TOPIC == entry.topic


def test_journal_entry_constructor_with_multiple_notes(today):
    notes = ["first note", "second note"]
    entry = JournalEntry(notes)
    assert "- first note\n- second note\n" == entry.note
    assert today == entry.date
    assert UNDEFINED_TOPIC == entry.topic


def test_journal_entry_constructor_with_note_and_date():
    note = "- a note"
    date = "2021-11-01"
    entry = JournalEntry(note, date)
    assert JournalEntry._parse_note(note) == entry.note
    assert date == entry.date
    assert UNDEFINED_TOPIC == entry.topic


def test_journal_entry_constructor_with_note_and_topic(today):
    note = "- a note"
    topic = "topic1"
    entry = JournalEntry(note, topic=topic)
    assert JournalEntry._parse_note(note) == entry.note
    assert today == entry.date
    assert topic == entry.topic


def test_parse_none_note():
    note = None
    parsed_note = JournalEntry._parse_note(note)
    assert "" == parsed_note


def test_parse_empty_note():
    note = ""
    parsed_note = JournalEntry._parse_note(note)
    assert "" == parsed_note


def test_parse_one_line_note_no_dash():
    note = "a note"
    parsed_note = JournalEntry._parse_note(note)
    assert "- a note\n" == parsed_note


def test_parse_one_line_note_with_dash():
    note = "- a note"
    parsed_note = JournalEntry._parse_note(note)
    assert "- a note\n" == parsed_note


def test_multiline_note():
    note = "- a note\n- with two lines"
    parsed_note = JournalEntry._parse_note(note)
    assert "- a note\n- with two lines\n" == parsed_note


def test_multiline_note_without_dash():
    note = "a note\nwith two lines"
    parsed_note = JournalEntry._parse_note(note)
    assert "- a note\nwith two lines\n" == parsed_note


def test_entry_from_string_multiple_notes_with_date_and_topic():
    txt_input = (
        "12nov2021: topic1 is this . first bullet , second bullet , third bullet"
    )
    entry = JournalEntry.from_string(txt_input)
    assert "2021-11-12" == entry.date
    assert "topic1 is this" == entry.topic
    assert "- first bullet\n- second bullet\n- third bullet\n" == entry.note


@mock.patch("jrnlmd.ioutils.input_from_editor")
def test_entry_from_string_with_user_input(mock_input_from_editor):
    mock_input_from_editor.return_value = "a note"
    txt_input = "12nov2021: topic1"
    entry = JournalEntry.from_string(txt_input, prompt_for_input=True)
    assert "2021-11-12" == entry.date
    assert "topic1" == entry.topic
    assert "- a note\n" == entry.note


def test_entry_to_dict():
    note = "- a note\n"
    date = "2021-11-01"
    topic = "topic1"
    entry = JournalEntry(note, date, topic)
    assert {date: {topic: note}} == entry._to_dict()
