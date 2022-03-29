from click.testing import CliRunner

from jrnlmd import jrnlmd


def test_cat_full_journal(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(jrnlmd.cli, ["-j", str(journal_multidate_file), "top"])
    assert (
        """topic1
topic2
"""
        == result.output
    )
