import pytest
from click.testing import CliRunner

from jrnlmd import jrnlmd


def test_cat_new_journal(new_journal_file):
    runner = CliRunner()
    result = runner.invoke(jrnlmd.cli, ["-j", str(new_journal_file), "cat"])
    assert "\n" == result.output


def test_cat_full_journal(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(jrnlmd.cli, ["-j", str(journal_multidate_file), "cat"])
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


def test_cat_specific_date(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(
        jrnlmd.cli, ["-j", str(journal_multidate_file), "cat", "2021-11-05:"]
    )
    assert (
        """# 2021-11-05

## topic1

- second date note

"""
        == result.output
    )


def test_cat_specific_topic(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(
        jrnlmd.cli, ["-j", str(journal_multidate_file), "cat", "topic2"]
    )
    assert (
        """# 2021-11-01

## topic2

- first date note

"""
        == result.output
    )


def test_cat_specific_date_and_topic(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(
        jrnlmd.cli, ["-j", str(journal_multidate_file), "cat", "1 11 2021: topic1"]
    )
    assert (
        """# 2021-11-01

## topic1

- another note

"""
        == result.output
    )


def test_cat_specific_topic_simplified(journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(
        jrnlmd.cli, ["-j", str(journal_multidate_file), "cat", "--simplified", "topic1"]
    )
    assert (
        """# topic1

## 2021-11-01

- another note

## 2021-11-05

- second date note

## 2021-11-10

- third date note

"""
        == result.output
    )


@pytest.mark.parametrize("mod", ["from", "since"])
def test_cat_journal_since(mod, journal_multidate_file):
    runner = CliRunner()
    result = runner.invoke(
        jrnlmd.cli,
        [
            "-j",
            str(journal_multidate_file),
            "cat",
            "--simplified",
            f"{mod} 2021-11-05:",
        ],
    )
    assert (
        """# 2021-11-05

## topic1

- second date note

# 2021-11-10

## topic1

- third date note

"""
        == result.output
    )
