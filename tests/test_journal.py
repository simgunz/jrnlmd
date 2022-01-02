from jrnlmd.journal import Journal


def test_create_empty_journal():
    journal = Journal()
    assert journal._j is not None
