import pytest

from jrnlmd.jrnlmd import md_to_dict


def test_md_to_dict_one_level():
    text = """
# 2021-01-01
## topic1

- first line
- second line
"""
    d = md_to_dict(text)
    assert {"2021-01-01": {"topic1": "- first line\n- second line\n"}} == d


def test_md_to_dict_two_topics():
    text = """
# 2021-01-01
## topic1

- first line
- second line

## topic2

- third line
"""
    d = md_to_dict(text)
    assert {
        "2021-01-01": {
            "topic1": "- first line\n- second line\n",
            "topic2": "- third line\n",
        }
    } == d


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
    d = md_to_dict(text)
    assert {
        "2021-01-01": {
            "topic1": (
                "- first line\n  wrapped\n- second line\n  ```bash\n  sudo pacman -S"
                " bash\n  ```\n"
            )
        }
    } == d


def test_md_to_dict_malformed_journal():
    text = """
## topic1

- first line
- second line
"""
    with pytest.raises(ValueError):
        md_to_dict(text)


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
    d = md_to_dict(text)
    assert {
        "2021-01-01": {
            "topic1": (
                "- first line\n  wrapped\n- second line\n  ```bash\n  # comment\n  sudo"
                " pacman -S bash\n  ```\n"
            )
        }
    } == d


def test_md_to_dict_line_continuation():
    text = """
# 2021-01-01
## topic1

- first line
line continuation
- second line
"""
    d = md_to_dict(text)
    assert {
        "2021-01-01": {"topic1": "- first line\nline continuation\n- second line\n"}
    } == d
