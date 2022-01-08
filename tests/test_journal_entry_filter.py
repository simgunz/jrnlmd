from jrnlmd.journal_entry_filter import JournalEntryFilter


def test_journal_entry_filter_constructor_with_topic():
    topic = "topic1"
    entry_filter = JournalEntryFilter(topic=topic)
    assert entry_filter.date is None
    assert topic == entry_filter.topic


def test_journal_entry_filter_constructor_with_date():
    date = "2021-11-01"
    entry_filter = JournalEntryFilter(date=date)
    assert date == entry_filter.date
    assert entry_filter.topic is None


def test_journal_entry_filter_from_string():
    date = "2021-11-01"
    topic = "topic1"
    entry_filter = JournalEntryFilter.from_string(f"{date}: {topic}")
    assert date == entry_filter.date
    assert topic == entry_filter.topic
