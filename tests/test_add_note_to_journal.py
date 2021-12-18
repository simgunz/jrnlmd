from jrnlmd.jrnlmd import add_note_to_journal


def test_add_note_to_new_journal(journal):
    add_note_to_journal(
        journal, ["12nov2021", "topic1", ".", "a", "note", ",", "second", "bullet"]
    )

    result = journal.read_text()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
        == result
    )


def test_add_note_to_existing_journal(dummy_journal):
    add_note_to_journal(
        dummy_journal,
        ["12nov2021", "topic1", ".", "appended", "note"],
    )
    result = dummy_journal.read_text()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet
- appended note
"""
        == result
    )
