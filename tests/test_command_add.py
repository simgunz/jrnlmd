from unittest import mock

from click.testing import CliRunner

from jrnlmd import jrnlmd
from jrnlmd.journal import Journal


@mock.patch("jrnlmd.ioutils.input_from_editor")
def test_add_note_from_user_input_to_new_journal(
    mock_input_from_editor, new_journal_file
):
    runner = CliRunner()
    mock_input_from_editor.return_value = "first note"

    runner.invoke(
        jrnlmd.cli, ["-j", str(new_journal_file), "add", "12 nov 2021: topic1"]
    )

    result = Journal(new_journal_file).to_md()
    assert (
        """# 2021-11-12

## topic1

- first note
"""
        == result
    )


@mock.patch("jrnlmd.ioutils.input_from_editor")
def test_add_note_from_empty_user_input_to_new_journal(
    mock_input_from_editor, new_journal_file
):
    runner = CliRunner()
    mock_input_from_editor.return_value = ""

    runner.invoke(
        jrnlmd.cli, ["-j", str(new_journal_file), "add", "12 nov 2021: topic1"]
    )

    result = Journal(new_journal_file).to_md()
    assert "" == result


def test_add_note_without_date(new_journal_file, today):
    runner = CliRunner()

    runner.invoke(jrnlmd.cli, ["-j", str(new_journal_file), "add", "topic1 . a note"])

    result = Journal(new_journal_file).to_md()
    assert (
        f"""# {today}

## topic1

- a note
"""
        == result
    )


@mock.patch("jrnlmd.ioutils.input_from_editor")
def test_add_note_without_a_topic(mock_input_from_editor, new_journal_file, today):
    runner = CliRunner()
    mock_input_from_editor.return_value = "a note"

    runner.invoke(jrnlmd.cli, ["-j", str(new_journal_file), "add"])

    result = Journal(new_journal_file).to_md()
    assert (
        f"""# {today}

## ungrouped

- a note
"""
        == result
    )


def test_add_note_to_new_journal(new_journal_file):
    runner = CliRunner()

    runner.invoke(
        jrnlmd.cli,
        [
            "-j",
            str(new_journal_file),
            "add",
            "12nov2021 : topic1 . a note , second bullet",
        ],
    )

    result = Journal(new_journal_file).to_md()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
        == result
    )


def test_add_note_to_existing_journal(simple_journal_file):
    runner = CliRunner()

    runner.invoke(
        jrnlmd.cli,
        [
            "-j",
            str(simple_journal_file),
            "add",
            "12nov2021 : topic1 . appended note",
        ],
    )

    result = Journal(simple_journal_file).to_md()
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
    runner = CliRunner()

    runner.invoke(
        jrnlmd.cli,
        [
            "-j",
            str(simple_journal_file),
            "add",
            "20nov2021 : topic1 . another note",
        ],
    )

    result = Journal(simple_journal_file).to_md()
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


def test_add_note_print_to_stdout(new_journal_file):
    runner = CliRunner()

    result = runner.invoke(
        jrnlmd.cli,
        ["-j", str(new_journal_file), "add", "2021-11-01: topic1 . a note"],
    )

    assert (
        """# 2021-11-01

## topic1

- a note

"""
        == result.output
    )
