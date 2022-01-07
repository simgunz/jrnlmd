from jrnlmd.journal_entry import JournalEntry


def test_journal_entry_constructor_note_only():
    note = "a note"
    entry = JournalEntry(note)
    assert note == entry.note
