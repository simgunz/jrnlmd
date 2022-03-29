from click.testing import CliRunner

from jrnlmd import jrnlmd
from jrnlmd.journal import Journal


def test_delete_specific_date(simple_journal_file):
    runner = CliRunner()
    result = runner.invoke(
        jrnlmd.cli, ["-j", str(simple_journal_file), "del", "2021-11-12:"]
    )
    journal = Journal(simple_journal_file)
    assert {} == journal._j
    assert (
        """Deleted entries:

# 2021-11-12

## topic1

- a note
- second bullet

"""
        == result.output
    )


def test_delete_specific_topic_on_date(journal_multidate_file):
    runner = CliRunner()
    runner.invoke(
        jrnlmd.cli, ["-j", str(journal_multidate_file), "del", "2021-11-01: topic1"]
    )
    journal = Journal(journal_multidate_file)
    assert {
        "2021-11-10": {"topic1": "- third date note\n"},
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-01": {"topic2": "- first date note\n"},
    } == journal._j


def test_delete_specific_topic_raises(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(
        jrnlmd.cli, ["-j", str(journal_multidate_file), "del", "topic1"]
    )
    assert "ERROR" in result.output
