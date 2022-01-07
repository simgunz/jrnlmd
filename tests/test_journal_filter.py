def test_journal_on_date(journal_multidate):
    journal_filtered = journal_multidate.on("2021-11-05")
    assert {"2021-11-05": {"topic1": "- second date note\n"}} == journal_filtered._j


def test_journal_on_date_not_present(journal_multidate):
    journal_filtered = journal_multidate.on("1999-11-05")
    assert {} == journal_filtered._j


def test_journal_since_date(journal_multidate):
    journal_filtered = journal_multidate.since("2021-11-05")
    assert {
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-10": {"topic1": "- third date note\n"},
    } == journal_filtered._j


def test_journal_since_future_date(journal_multidate):
    journal_filtered = journal_multidate.since("3000-11-05")
    assert {} == journal_filtered._j


def test_journal_about_topic(journal_multidate):
    journal_filtered = journal_multidate.about("topic1")
    assert {
        "2021-11-01": {"topic1": "- another note\n"},
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-10": {"topic1": "- third date note\n"},
    } == journal_filtered._j


def test_journal_about_topic_not_present(journal_multidate):
    journal_filtered = journal_multidate.about("nothing")
    assert {} == journal_filtered._j


def test_journal_about_topic_partial_matching(journal_multidate):
    journal_filtered = journal_multidate.about("pic1")
    assert {
        "2021-11-01": {"topic1": "- another note\n"},
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-10": {"topic1": "- third date note\n"},
    } == journal_filtered._j
