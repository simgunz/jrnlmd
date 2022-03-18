from jrnlmd.parsers import (
    _parse_date,
    _split_date_topic,
    _split_on_separator,
    parse_journal_entry_text,
)


def test_parse_date():
    txt_date = "12nov2021"
    iso_date = _parse_date(txt_date)
    assert "2021-11-12" == iso_date


def test_parse_date_unparsable():
    txt_date = "aaaa"
    iso_date = _parse_date(txt_date)
    assert iso_date is None


def test_parse_date_single_char():
    txt_date = "a"
    iso_date = _parse_date(txt_date)
    assert iso_date is None


def test_parse_date_iso_format():
    txt_date = "2021-11-12"
    iso_date = _parse_date(txt_date)
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


def test_split_with_no_delimiter():
    text = "word1 word2 word3"
    result = _split_on_separator(text, sep=".")
    assert [text] == result


def test_split_with_one_delimiter():
    text = "word1 . word2 word3"
    result = _split_on_separator(text, sep=".")
    assert ["word1", "word2 word3"] == result


def test_split_with_delimiter_not_surrounded_by_left_space():
    text = "word1. word2 word3"
    result = _split_on_separator(text, sep=".")
    assert ["word1. word2 word3"] == result


def test_split_with_delimiter_not_surrounded_by_right_space():
    text = "word1 .word2 word3"
    result = _split_on_separator(text, sep=".")
    assert ["word1 .word2 word3"] == result


def test_input_single_note_with_colon_in_note():
    txt_input = "topic1 . he said: hello"
    date, topic, notes = parse_journal_entry_text(txt_input)
    assert date is None
    assert "topic1" == topic
    assert ["he said: hello"] == notes


def test_split_date_topic():
    text = "12 nov: topic1"
    date, topic = _split_date_topic(text)
    assert "12 nov" == date
    assert "topic1" == topic


def test_split_date_topic_only_topic():
    text = "topic1"
    date, topic = _split_date_topic(text)
    assert "" == date
    assert "topic1" == topic


def test_split_date_topic_only_date():
    text = "12 nov:"
    date, topic = _split_date_topic(text)
    assert "12 nov" == date
    assert "" == topic
