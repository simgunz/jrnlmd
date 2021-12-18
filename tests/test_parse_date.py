from jrnlmd.jrnlmd import parse_date


def test_date_parser():
    txt_date = "12nov2021"
    iso_date = parse_date(txt_date)
    assert "2021-11-12" == iso_date


def test_date_parser_unparsable():
    txt_date = "aaaa"
    iso_date = parse_date(txt_date)
    assert None == iso_date


def test_date_parser_single_char():
    txt_date = "a"
    iso_date = parse_date(txt_date)
    assert None == iso_date
