from jrnlmd.jrnlmd import command_del


def test_delete_specific_date(simple_journal):
    command_del(simple_journal, "2021-11-12:")
    assert {} == simple_journal._j


def test_delete_specific_topic_on_date(journal_multidate):
    command_del(journal_multidate, "2021-11-01: topic1")
    assert {
        "2021-11-10": {"topic1": "- third date note\n"},
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-01": {"topic2": "- first date note\n"},
    } == journal_multidate._j


def test_delete_specific_topic_raises(journal_multidate):
    command_del(journal_multidate, "topic1")
