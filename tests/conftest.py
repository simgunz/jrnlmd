from unittest import mock

import pytest


@pytest.fixture()
def empty_journal(tmp_path):
    return tmp_path / "journal.md"


@pytest.fixture()
def dummy_journal(empty_journal):
    empty_journal.write_text(
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
    )
    return empty_journal


@pytest.fixture()
def journal_multidate(empty_journal):
    empty_journal.write_text(
        """# 2021-11-10

## topic1

- third date note

# 2021-11-05

## topic1

- second date note

# 2021-11-01

## topic2

- first date note

## topic1

- another note
"""
    )
    return empty_journal


# Replace print_with_external with print
@pytest.fixture(autouse=True)
def print_with_external_mock():
    with mock.patch("jrnlmd.jrnlmd.print_with_external", wraps=print) as print_mock:
        yield print_mock
