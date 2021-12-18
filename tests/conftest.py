import pytest


@pytest.fixture()
def journal(tmp_path):
    return tmp_path / "journal.md"


@pytest.fixture()
def dummy_journal(journal):
    journal.write_text(
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
    )
    return journal


@pytest.fixture()
def journal_multidate(journal):
    journal.write_text(
        """# 2021-11-01

## topic1

- first date note

# 2021-11-05

## topic1

- second date note

# 2021-11-10

## topic1

- third date note
"""
    )
    return journal
