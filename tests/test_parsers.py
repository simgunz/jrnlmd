from jrnlmd.parsers import (
    join_notes_tokens,
    parse_date,
    parse_input,
    parse_note,
    split_list_on_delimiter,
)


def test_join_notes_tokens():
    notes_tokens = [["word1"], ["word2", "word3"]]
    result = join_notes_tokens(notes_tokens)
    assert "- word1\n- word2 word3\n" == result


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


def test_parse_one_line_note_no_dash():
    note = "a note"
    parsed_note = parse_note(note)
    assert "- a note\n" == parsed_note


def test_parse_one_line_note_with_dash():
    note = "- a note"
    parsed_note = parse_note(note)
    assert "- a note\n" == parsed_note


def test_multiline_note():
    note = "- a note\n- with two lines"
    parsed_note = parse_note(note)
    assert "- a note\n- with two lines\n" == parsed_note


def test_multiline_note_without_dash():
    note = "a note\nwith two lines"
    parsed_note = parse_note(note)
    assert "- a note\nwith two lines\n" == parsed_note


def test_input_date_only():
    txt_input = "12 nov 2021:"
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert topic is None
    assert note is None


def test_input_single_note_with_topic_only():
    txt_input = "topic1 is this"
    date, topic, note = parse_input(txt_input)
    assert date is None
    assert "topic1 is this" == topic
    assert note is None


def test_input_single_note_with_topic():
    txt_input = "topic1 is this . a note"
    date, topic, note = parse_input(txt_input)
    assert date is None
    assert "topic1 is this" == topic
    assert "- a note\n" == note


def test_input_single_note_with_date_and_topic():
    txt_input = "12nov2021: topic1 is this . a note"
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert "- a note\n" == note


def test_input_single_note_with_date_with_space_and_topic():
    txt_input = "12 nov 2021: topic1 is this . a note"
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert "- a note\n" == note


def test_input_multiple_notes_with_date_and_topic():
    txt_input = (
        "12nov2021: topic1 is this . first bullet , second bullet , third bullet"
    )
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert "- first bullet\n- second bullet\n- third bullet\n" == note
