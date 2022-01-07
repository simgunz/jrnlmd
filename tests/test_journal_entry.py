from jrnlmd.journal_entry import UNDEFINED_TOPIC, JournalEntry


def test_journal_entry_constructor_note_only(today):
    note = "a note"
    entry = JournalEntry(note)
    assert note == entry.note
    assert today == entry.date
    assert UNDEFINED_TOPIC == entry.topic


def test_journal_entry_constructor_with_note_and_date():
    note = "a note"
    date = "2021-11-01"
    entry = JournalEntry(note, date)
    assert note == entry.note
    assert date == entry.date
    assert UNDEFINED_TOPIC == entry.topic
