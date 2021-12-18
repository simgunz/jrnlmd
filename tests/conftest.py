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
