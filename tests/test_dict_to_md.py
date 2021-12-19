from jrnlmd.jrnlmd import dict_to_md


def test_dict_to_md_one_level():
    d = {"2021-01-01": {"topic1": "- first line\n- second line\n"}}
    text = dict_to_md(d)
    assert (
        """# 2021-01-01

## topic1

- first line
- second line
"""
        == text
    )


def test_dict_to_md_comment_in_code_fence():
    d = {
        "2021-01-01": {
            "topic1": (
                "- first line\n  wrapped\n- second line\n  ```bash\n  # comment\n  sudo"
                " pacman -S bash\n  ```\n"
            )
        }
    }
    text = dict_to_md(d)
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
    d = {
        "2021-01-01": {"topic1": "- first line\n- second line\n"},
        "2021-01-02": {
            "topic2": "- third line\n",
            "topic3": "- fourth line\n- fifth line\n",
        },
    }
    text = dict_to_md(d)
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
