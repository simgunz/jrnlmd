from jrnlmd.parsers import parse_date, parse_journal_entry_text, split_list_on_delimiter


def test_split_with_no_delimiter():
    tokens = ["word1", "word2", "word3"]
    result = split_list_on_delimiter(tokens, delimiter=".")
    assert [["word1", "word2", "word3"]] == result


def test_split_with_one_delimiter():
    tokens = ["word1", ".", "word2", "word3"]
    result = split_list_on_delimiter(tokens, delimiter=".")
    assert [["word1"], ["word2", "word3"]] == result


def test_parse_date():
    txt_date = "12nov2021"
    iso_date = parse_date(txt_date)
    assert "2021-11-12" == iso_date


def test_parse_date_unparsable():
    txt_date = "aaaa"
    iso_date = parse_date(txt_date)
    assert iso_date is None


def test_parse_date_single_char():
    txt_date = "a"
    iso_date = parse_date(txt_date)
    assert iso_date is None


def test_parse_date_iso_format():
    txt_date = "2021-11-12"
    iso_date = parse_date(txt_date)
    assert "2021-11-12" == iso_date


def test_input_date_only():
    txt_input = "12 nov 2021:"
    date, topic, notes = parse_journal_entry_text(txt_input)
    assert "2021-11-12" == date
    assert topic is None
    assert notes is None


def test_input_single_note_with_topic_only():
    txt_input = "topic1 is this"
    date, topic, notes = parse_journal_entry_text(txt_input)
    assert date is None
    assert "topic1 is this" == topic
    assert notes is None


def test_input_single_note_with_topic():
    txt_input = "topic1 is this . a note"
    date, topic, notes = parse_journal_entry_text(txt_input)
    assert date is None
    assert "topic1 is this" == topic
    assert ["a note"] == notes


def test_input_single_note_with_date_and_topic():
    txt_input = "12nov2021: topic1 is this . a note"
    date, topic, notes = parse_journal_entry_text(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert ["a note"] == notes


def test_input_single_note_with_date_with_space_and_topic():
    txt_input = "12 nov 2021: topic1 is this . a note"
    date, topic, notes = parse_journal_entry_text(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert ["a note"] == notes


def test_input_multiple_notes_with_date_and_topic():
    txt_input = (
        "12nov2021: topic1 is this . first bullet , second bullet , third bullet"
    )
    date, topic, notes = parse_journal_entry_text(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert ["first bullet", "second bullet", "third bullet"] == notes
