from unittest import mock

from jrnlmd.jrnlmd import command_add


@mock.patch("jrnlmd.jrnlmd.input_from_editor")
def test_add_note_from_user_input_to_new_journal(
    mock_input_from_editor, new_journal_file
):
    mock_input_from_editor.return_value = "first note"
    command_add(new_journal_file, "12 nov 2021: topic1")

    result = new_journal_file.read_text()
    assert (
        """# 2021-11-12

## topic1

- first note
"""
        == result
    )


def test_add_note_without_date(new_journal_file, today):
    command_add(new_journal_file, "topic1 . a note")

    result = new_journal_file.read_text()
    assert (
        f"""# {today}

## topic1

- a note
"""
        == result
    )


@mock.patch("jrnlmd.jrnlmd.input_from_editor")
def test_add_note_without_a_topic(mock_input_from_editor, new_journal_file, today):
    mock_input_from_editor.return_value = "a note"
    command_add(new_journal_file, "")

    result = new_journal_file.read_text()
    assert (
        f"""# {today}

## ungrouped

- a note
"""
        == result
    )


def test_add_note_to_new_journal(new_journal_file):
    command_add(new_journal_file, "12nov2021 : topic1 . a note , second bullet")

    result = new_journal_file.read_text()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
        == result
    )


def test_add_note_to_existing_journal(simple_journal_file):
    command_add(
        simple_journal_file,
        "12nov2021 : topic1 . appended note",
    )
    result = simple_journal_file.read_text()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet
- appended note
"""
        == result
    )


def test_add_note_different_date_to_existing_journal(simple_journal_file):
    command_add(
        simple_journal_file,
        "20nov2021 : topic1 . another note",
    )
    result = simple_journal_file.read_text()
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
