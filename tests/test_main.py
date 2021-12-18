import pytest
from jrnlmd.jrnlmd import main


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


def test_main_create_new_journal(journal):
    args = [
        "--journal",
        str(journal),
        "add",
        "12nov2021 topic1 . a note , second bullet",
    ]
    main(args)
    result = journal.read_text()
    assert (
        result
        == """# 2021-11-12

## topic1

- a note
- second bullet
"""
    )


def test_main_append_to_journal(dummy_journal):
    args2 = [
        "--journal",
        str(dummy_journal),
        "add",
        "12nov2021 topic2 . appended note",
    ]
    main(args2)
    result = dummy_journal.read_text()
    assert result == (
        """# 2021-11-12

## topic1

- a note
- second bullet

## topic2

- appended note
"""
    )
