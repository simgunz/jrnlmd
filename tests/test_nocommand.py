from click.testing import CliRunner

from jrnlmd import jrnlmd
from jrnlmd.journal import Journal


def test_nocommand_and_no_arguments_invoke_cat(mocker, journal_multidate_file):
    mock_cat = mocker.patch("jrnlmd.jrnlmd.cat")
    runner = CliRunner()

    runner.invoke(jrnlmd.cli, ["-j", str(journal_multidate_file)])

    mock_cat.assert_called_with(filter_="")


def test_nocommand_and_arguments_invoke_add(today, new_journal_file):
    runner = CliRunner()

    runner.invoke(jrnlmd.cli, ["-j", str(new_journal_file), "topic1 . a note"])

    result = Journal(new_journal_file).to_md()
    assert (
        f"""# {today}

## topic1

- a note
"""
        == result
    )
