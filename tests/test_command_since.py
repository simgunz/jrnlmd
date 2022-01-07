import pytest

from jrnlmd.jrnlmd import command_since


@pytest.mark.skip
def test_cat_journal_since(journal_multidate_file, capsys):
    command_since(journal_multidate_file, "2021-11-05")
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
