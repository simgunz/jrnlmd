def test_journal_on_date(journal_multidate):
    journal_filtered = journal_multidate.on("2021-11-05")
    assert {"2021-11-05": {"topic1": "- second date note\n"}} == journal_filtered._j


def test_journal_on_date_not_present(journal_multidate):
    journal_filtered = journal_multidate.on("1999-11-05")
    assert {} == journal_filtered._j
