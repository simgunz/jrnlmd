from collections import defaultdict

from jrnlmd.journal import Journal


def test_create_empty_journal():
    journal = Journal()
    assert isinstance(journal._j, defaultdict)


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
