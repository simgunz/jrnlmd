import pytest
import tempfile
import unittest

from jrnlmd.jrnlmd import md_to_dict


def write_md_file(text):
    f = tempfile.mktemp()
    open(f, "w").write(text)


class TestMdConversion(unittest.TestCase):
    def test_md_to_dict(self):
        text = """
# 2021-01-01
## topic1

- first line
- second line
"""
        d = md_to_dict(text)
        self.assertEqual({"2021-01-01": {"topic1": "- first line\n- second line\n"}}, d)

    def test_md_to_dict_two_topics(self):
        text = """
# 2021-01-01
## topic1

- first line
- second line

## topic2

- third line
"""
        d = md_to_dict(text)
        self.assertEqual(
            {
                "2021-01-01": {
                    "topic1": "- first line\n- second line\n",
                    "topic2": "- third line\n",
                }
            },
            d,
        )

    def test_md_to_dict_wrapped_lines(self):
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
        self.assertEqual(
            {
                "2021-01-01": {
                    "topic1": "- first line\n  wrapped\n- second line\n  ```bash\n  sudo pacman -S bash\n  ```\n"
                }
            },
            d,
        )

    def test_md_to_dict_malformed_journal(self):
        text = """
## topic1

- first line
- second line
"""
        with pytest.raises(ValueError):
            md_to_dict(text)