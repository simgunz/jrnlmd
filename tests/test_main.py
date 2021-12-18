import tempfile
import unittest

import pytest
from jrnlmd.jrnlmd import main


@pytest.fixture(scope="class")
def dummy_journal(request):
    request.cls.dummy_journal = """# 2021-11-12

## topic1

- a note
- second bullet
"""


@pytest.mark.usefixtures("dummy_journal")
class TestMain(unittest.TestCase):
    def setUp(self):
        self.journal = tempfile.NamedTemporaryFile(mode="w+")

    def tearDown(self):
        self.journal.close()

    def test_main_create_new_journal(self):
        args = [
            "--journal",
            self.journal.name,
            "add",
            "12nov2021 topic1 . a note , second bullet",
        ]
        main(args)
        self.assertEqual(
            """# 2021-11-12

## topic1

- a note
- second bullet
""",
            self.journal.read(),
        )

    def test_main_append_to_journal(self):
        self.journal.write(self.dummy_journal)
        self.journal.seek(0)
        args2 = [
            "--journal",
            self.journal.name,
            "add",
            "12nov2021 topic2 . appended note",
        ]
        main(args2)
        self.journal.seek(0)
        self.assertEqual(
            """# 2021-11-12

## topic1

- a note
- second bullet

## topic2

- appended note
""",
            self.journal.read(),
        )
