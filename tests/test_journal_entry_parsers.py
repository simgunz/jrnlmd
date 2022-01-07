from jrnlmd.journal_entry import JournalEntry


def test_parse_date():
    txt_date = "12nov2021"
    iso_date = JournalEntry.parse_date(txt_date)
    assert "2021-11-12" == iso_date


def test_parse_date_unparsable():
    txt_date = "aaaa"
    iso_date = JournalEntry.parse_date(txt_date)
    assert iso_date is None


def test_parse_date_single_char():
    txt_date = "a"
    iso_date = JournalEntry.parse_date(txt_date)
    assert iso_date is None


def test_parse_date_iso_format():
    txt_date = "2021-11-12"
    iso_date = JournalEntry.parse_date(txt_date)
    assert "2021-11-12" == iso_date
