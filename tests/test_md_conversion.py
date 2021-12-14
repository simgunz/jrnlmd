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
        self.assertEqual({"2021-01-01": {"topic1": ["first line", "second line"]}}, d)
