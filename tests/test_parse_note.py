from jrnlmd.parsers import parse_note


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
