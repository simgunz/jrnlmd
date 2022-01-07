from jrnlmd.journal_entry import UNDEFINED_TOPIC, JournalEntry


def test_journal_entry_constructor_note_only(today):
    note = "a note"
    entry = JournalEntry(note)
    assert note == entry.note
    assert today == entry.date
    assert UNDEFINED_TOPIC == entry.topic
