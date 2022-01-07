from collections import defaultdict
from pathlib import Path

import pytest

from jrnlmd.journal import Journal


def test_create_new_journal_file():
    journal = Journal()
    assert isinstance(journal._j, defaultdict)


def test_constructor_with_journal_path(new_journal_file):
    journal = Journal(new_journal_file)
    assert new_journal_file == journal._journal_path


def test_load_not_existing_file():
    journal_file = Path("/tmp/not_existing.md")
    journal = Journal(journal_file)
    with pytest.raises(FileNotFoundError):
        journal.load()


def test_from_dict():
    d = {
        "2021-01-01": {"topic1": "- first line\n- second line\n"},
        "2021-01-02": {
            "topic2": "- third line\n",
            "topic3": "- fourth line\n- fifth line\n",
        },
    }
    journal = Journal.from_dict(d)
    assert d == journal._j
    assert isinstance(journal._j, defaultdict)
    assert isinstance(journal._j["2021-01-01"], defaultdict)


def test_dict_to_md_one_level():
    journal = Journal.from_dict(
        {"2021-01-01": {"topic1": "- first line\n- second line\n"}}
    )
    text = journal.to_md()
    assert (
        """# 2021-01-01

## topic1

- first line
- second line
"""
        == text
    )


def test_dict_to_md_comment_in_code_fence():
    journal = Journal.from_dict(
        {
            "2021-01-01": {
                "topic1": (
                    "- first line\n  wrapped\n- second line\n  ```bash\n  # comment\n "
                    " sudo pacman -S bash\n  ```\n"
                )
            }
        }
    )
    text = journal.to_md()
    assert (
        """# 2021-01-01

## topic1

- first line
  wrapped
- second line
  ```bash
  # comment
  sudo pacman -S bash
  ```
"""
        == text
    )


def test_dict_to_md_two_levels():
    journal = Journal.from_dict(
        {
            "2021-01-01": {"topic1": "- first line\n- second line\n"},
            "2021-01-02": {
                "topic2": "- third line\n",
                "topic3": "- fourth line\n- fifth line\n",
            },
        }
    )
    text = journal.to_md()
    assert (
        """# 2021-01-02

## topic2

- third line

## topic3

- fourth line
- fifth line

# 2021-01-01

## topic1

- first line
- second line
"""
        == text
    )


def test_dict_to_md_compact():
    journal = Journal.from_dict(
        {
            "2021-01-01": {"topic1": "- first line\n- second line\n"},
            "2021-01-02": {
                "topic2": "- third line\n",
                "topic3": "- fourth line\n- fifth line\n",
            },
        }
    )
    text = journal.to_md(compact=True)
    assert (
        """# 2021-01-02
## topic2
- third line

## topic3
- fourth line
- fifth line

# 2021-01-01
## topic1
- first line
- second line
"""
        == text
    )


def test_dict_to_md_date_ascending():
    journal = Journal.from_dict(
        {
            "2021-01-01": {"topic1": "- first line\n- second line\n"},
            "2021-01-02": {
                "topic2": "- third line\n",
            },
        }
    )
    text = journal.to_md(date_descending=False)
    assert (
        """# 2021-01-01

## topic1

- first line
- second line

# 2021-01-02

## topic2

- third line
"""
        == text
    )


def test_dict_to_md_simplified():
    journal = Journal.from_dict(
        {
            "2021-01-01": {"topic1": "- first line\n"},
            "2021-01-02": {
                "topic1": "- second line\n",
            },
        }
    )
    text = journal.to_md(date_descending=False, simplified=True)
    assert (
        """# 2021-01-01

- first line

# 2021-01-02

- second line
"""
        == text
    )


def test_md_to_dict_one_level():
    text = """
# 2021-01-01
## topic1

- first line
- second line
"""
    journal = Journal.from_md(text)
    assert {"2021-01-01": {"topic1": "- first line\n- second line\n"}} == journal._j


def test_md_to_dict_two_topics():
    text = """
# 2021-01-01
## topic1

- first line
- second line

## topic2

- third line
"""
    journal = Journal.from_md(text)
    assert {
        "2021-01-01": {
            "topic1": "- first line\n- second line\n",
            "topic2": "- third line\n",
        }
    } == journal._j


def test_md_to_dict_wrapped_lines():
    text = """
# 2021-01-01
## topic1

- first line
  wrapped
- second line
  ```bash
  sudo pacman -S bash
  ```
"""
    journal = Journal.from_md(text)
    assert {
        "2021-01-01": {
            "topic1": (
                "- first line\n  wrapped\n- second line\n  ```bash\n  sudo pacman -S"
                " bash\n  ```\n"
            )
        }
    } == journal._j


def test_md_to_dict_malformed_journal():
    text = """
## topic1

- first line
- second line
"""
    with pytest.raises(ValueError):
        Journal.from_md(text)


def test_md_to_dict_comment_in_code_fence():
    text = """
# 2021-01-01
## topic1

- first line
  wrapped
- second line
  ```bash
  # comment
  sudo pacman -S bash
  ```
"""
    journal = Journal.from_md(text)
    assert {
        "2021-01-01": {
            "topic1": (
                "- first line\n  wrapped\n- second line\n  ```bash\n  # comment\n  sudo"
                " pacman -S bash\n  ```\n"
            )
        }
    } == journal._j


def test_md_to_dict_line_continuation():
    text = """
# 2021-01-01
## topic1

- first line
line continuation
- second line
"""
    journal = Journal.from_md(text)
    assert {
        "2021-01-01": {"topic1": "- first line\nline continuation\n- second line\n"}
    } == journal._j


@pytest.mark.parametrize("code_fence", ["```", "~~~"])
def test_md_to_dict_with_unindented_comment_in_code_fence(code_fence):
    text = f"""
# 2021-01-01
## topic1

- first line
{code_fence}bash
# comment
sudo pacman -S bash
{code_fence}
- second line
"""
    journal = Journal.from_md(text)
    assert {
        "2021-01-01": {
            "topic1": (
                f"- first line\n{code_fence}bash\n# comment\nsudo pacman -S"
                f" bash\n{code_fence}\n- second line\n"
            )
        }
    } == journal._j
