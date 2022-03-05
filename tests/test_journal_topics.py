def test_journal_topics(journal_multidate):
    topics = journal_multidate.topics()
    assert ["topic1", "topic2"] == topics
