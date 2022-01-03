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
