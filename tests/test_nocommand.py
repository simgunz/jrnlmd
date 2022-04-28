from click.testing import CliRunner

from jrnlmd import jrnlmd


def test_nocommand_and_no_arguments_invoke_cat(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(jrnlmd.cli, ["-j", str(journal_multidate_file)])
    assert (
        """# 2021-11-01

## topic2

- first date note

## topic1

- another note

# 2021-11-05

## topic1

- second date note

# 2021-11-10

## topic1

- third date note

"""
        == result.output
    )
