import pytest

from jrnlmd.jrnlmd import command_cat


def test_cat_new_journal(new_journal, capsys):
    command_cat(new_journal)
    captured = capsys.readouterr()
    assert "\n" == captured.out


def test_cat_full_journal(journal_multidate, capsys):
    command_cat(journal_multidate)
    captured = capsys.readouterr()
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
        == captured.out
    )


def test_cat_specific_date(journal_multidate, capsys):
    command_cat(journal_multidate, "2021-11-05:")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-05

## topic1

- second date note

"""
        == captured.out
    )


def test_cat_specific_topic(journal_multidate, capsys):
    command_cat(journal_multidate, "topic2")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-01

## topic2

- first date note

"""
        == captured.out
    )


def test_cat_specific_date_and_topic(journal_multidate, capsys):
    command_cat(journal_multidate, "1 11 2021: topic1")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-01

## topic1

- another note

"""
        == captured.out
    )


def test_cat_specific_topic_simplified(journal_multidate, capsys):
    command_cat(journal_multidate, "topic1", simplified=True)
    captured = capsys.readouterr()
    assert (
        """# 2021-11-01

- another note

# 2021-11-05

- second date note

# 2021-11-10

- third date note

"""
        == captured.out
    )


@pytest.mark.parametrize("mod", ["from", "since"])
def test_cat_journal_since(mod, journal_multidate, capsys):
    command_cat(journal_multidate, f"{mod} 2021-11-05:")
    captured = capsys.readouterr()
    assert (
        """# 2021-11-05

## topic1

- second date note

# 2021-11-10

## topic1

- third date note

"""
        == captured.out
    )
