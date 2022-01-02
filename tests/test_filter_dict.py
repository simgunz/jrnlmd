from jrnlmd.jrnlmd import filter_dict_date, filter_dict_topic, md_to_dict


def test_filter_dict_equal_date(journal_multidate):
    journal_dict = md_to_dict(journal_multidate.read_text())
    filtered_dict = filter_dict_date(journal_dict, "2021-11-05")
    assert {"2021-11-05": {"topic1": "- second date note\n"}} == filtered_dict


def test_filter_dict_since_date(journal_multidate):
    journal_dict = md_to_dict(journal_multidate.read_text())
    filtered_dict = filter_dict_date(journal_dict, "2021-11-05", str.__ge__)
    assert {
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-10": {"topic1": "- third date note\n"},
    } == filtered_dict


def test_filter_dict_topic(journal_multidate):
    journal_dict = md_to_dict(journal_multidate.read_text())
    filtered_dict = filter_dict_topic(journal_dict, "topic1")
    assert {
        "2021-11-01": {"topic1": "- another note\n"},
        "2021-11-05": {"topic1": "- second date note\n"},
        "2021-11-10": {"topic1": "- third date note\n"},
    } == filtered_dict
