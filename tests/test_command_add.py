from jrnlmd.jrnlmd import command_add


def test_add_note_to_new_journal(journal):
    command_add(
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
    command_add(
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


def test_add_note_different_date_to_existing_journal(dummy_journal):
    command_add(
        dummy_journal,
        ["20nov2021", "topic1", ".", "another", "note"],
    )
    result = dummy_journal.read_text()
    assert (
        """# 2021-11-20

## topic1

- another note

# 2021-11-12

## topic1

- a note
- second bullet
"""
        == result
    )
