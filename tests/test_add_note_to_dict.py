import pytest

from jrnlmd.jrnlmd import add_note_to_dict


@pytest.fixture
def journal_dict():
    return {
        "2021-01-01": {"topic1": "- first line\n- second line\n"},
        "2021-01-02": {
            "topic2": "- third line\n",
            "topic3": "- fourth line\n- fifth line\n",
        },
    }


def test_add_note_to_dict(journal_dict):
    new_topic = "topic1"
    new_date = "2021-01-01"
    new_note = "- my note"
    add_note_to_dict(journal_dict, new_note, new_date, new_topic)
    assert {
        "2021-01-01": {"topic1": "- first line\n- second line\n- my note\n"},
        "2021-01-02": {
            "topic2": "- third line\n",
            "topic3": "- fourth line\n- fifth line\n",
        },
    } == journal_dict


def test_add_note_without_dash_to_dict(journal_dict):
    new_topic = "topic1"
    new_date = "2021-01-01"
    new_note = "my note"
    add_note_to_dict(journal_dict, new_note, new_date, new_topic)
    assert {
        "2021-01-01": {"topic1": "- first line\n- second line\n- my note\n"},
        "2021-01-02": {
            "topic2": "- third line\n",
            "topic3": "- fourth line\n- fifth line\n",
        },
    } == journal_dict
