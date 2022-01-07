import datetime
from unittest import mock

import pytest

from jrnlmd.journal import Journal


@pytest.fixture()
def new_journal_file(tmp_path):
    return tmp_path / "journal.md"


@pytest.fixture()
def empty_journal_file(new_journal_file):
    new_journal_file.touch()
    return new_journal_file


@pytest.fixture()
def simple_journal_file(new_journal_file):
    new_journal_file.write_text(
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
    )
    return new_journal_file


@pytest.fixture()
def journal_multidate_file(new_journal_file):
    new_journal_file.write_text(
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
    return new_journal_file


@pytest.fixture
def new_journal(new_journal_file):
    return Journal(new_journal_file)


@pytest.fixture
def simple_journal(simple_journal_file):
    return Journal(simple_journal_file)


@pytest.fixture
def journal_multidate(journal_multidate_file):
    journal = Journal(journal_multidate_file)
    journal.load()
    return journal


@pytest.fixture
def today():
    date_today = datetime.date.today()
    return date_today.strftime("%Y-%m-%d")


# Replace print_with_external with print
@pytest.fixture(autouse=True)
def print_with_external_mock():
    with mock.patch("jrnlmd.jrnlmd.print_with_external", wraps=print) as print_mock:
        yield print_mock
