from collections import defaultdict
from pathlib import Path

import pytest

from jrnlmd.journal import Journal
from jrnlmd.journal_entry import JournalEntry


def test_create_new_journal_file():
    journal = Journal()
    assert isinstance(journal._j, defaultdict)


def test_constructor_with_journal_path(new_journal_file):
    journal = Journal(new_journal_file)
    assert new_journal_file == journal._journal_file


def test_constructor_loads_journal_if_exists(simple_journal_file):
    journal = Journal(simple_journal_file)
    assert {"2021-11-12": {"topic1": "- a note\n- second bullet\n"}} == journal._j


def test_load_not_existing_file(new_journal_file):
    journal = Journal(new_journal_file)
    with pytest.raises(FileNotFoundError):
        journal.load()


def test_load_with_file_name_not_set():
    journal = Journal()
    with pytest.raises(RuntimeError, match="The journal file name has not been set."):
        journal.load()


def test_load_empty_journal(empty_journal_file):
    journal = Journal(empty_journal_file)
    journal.load()
    assert {} == journal._j


def test_load_journal(simple_journal_file):
    journal = Journal(simple_journal_file)
    journal.load()
    assert {"2021-11-12": {"topic1": "- a note\n- second bullet\n"}} == journal._j


def test_load_journal_twice(simple_journal_file):
    journal = Journal(simple_journal_file)
    journal.load()
    journal.load()
    assert {"2021-11-12": {"topic1": "- a note\n- second bullet\n"}} == journal._j


def test_save_with_file_name_not_set():
    journal = Journal()
    with pytest.raises(RuntimeError, match="The journal file name has not been set."):
        journal.save()


def test_save_new_journal_file_with_no_content(new_journal_file):
    journal = Journal(new_journal_file)
    journal.save()
    assert new_journal_file.is_file()


def test_save_new_journal_file(new_journal_file):
    journal = Journal.from_dict(
        {"2021-11-12": {"topic1": "- a note\n- second bullet\n"}}
    )
    journal.journal_file = new_journal_file
    journal.save()
    result = new_journal_file.read_text()
    assert (
        """# 2021-11-12

## topic1

- a note
- second bullet
"""
        == result
    )


def test_journal_file_setter_with_path(new_journal_file):
    journal = Journal()
    journal.journal_file = new_journal_file
    assert journal._journal_file == new_journal_file


def test_journal_file_setter_with_string():
    journal = Journal()
    journal.journal_file = "/tmp/journal_test.md"
    assert journal._journal_file == Path("/tmp/journal_test.md")


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


def test_add(new_journal):
    entry = JournalEntry("a note", "2021-11-01", "topic1")
    new_journal.add(entry)
    assert {"2021-11-01": {"topic1": "- a note\n"}} == new_journal._j


def test_delete_date(simple_journal):
    simple_journal.delete("2021-11-12")
    assert {} == simple_journal._j


def test_delete_missing_date(simple_journal):
    with pytest.raises(KeyError):
        simple_journal.delete("3000-11-11")


def test_delete_topic_on_date(journal_multidate):
    deleted_entries = journal_multidate.delete("2021-11-01", "topic1")
    assert {
        "2021-11-10": {"topic1": "- third date note\n"},
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-01": {"topic2": "- first date note\n"},
    } == journal_multidate._j
    assert (
        """# 2021-11-01

## topic1

- another note
"""
        == deleted_entries.to_md()
    )


def test_delete_missing_topic(simple_journal):
    with pytest.raises(KeyError):
        simple_journal.delete("2021-11-12", "missing_topic")


def test_delete_last_topic_on_date(simple_journal):
    simple_journal.delete("2021-11-12", "topic1")
    assert {} == simple_journal._j


def test_from_md_preserves_blank_lines_in_code_fence():
    in_text_md = """# 2021-11-01

## topic1

- a note
- second note:
```bash
# comment
ls -a

mkdir test
```
"""
    journal = Journal.from_md(in_text_md)
    out_text_md = journal.to_md()
    assert in_text_md == out_text_md
